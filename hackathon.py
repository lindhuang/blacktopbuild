#!/usr/bin/env python3

import math

from PIL import Image

# VARIOUS FILTERS

#helper functions for greyscale image:
def get_pixel(image, x, y):
    # print(image['pixels'][(y)*(image['width'])+(x)])
    return image['pixels'][(y)*(image['width'])+(x)]


def set_pixel(image, x, y, c):
    image['pixels'][(y)*(image['width'])+(x)]=c


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    for y in range(image['height']):
        for x in range(image['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            result['pixels'].append(newcolor)
    return result



# HELPER FUNCTIONS

def correlate(image, kernel):

    kwidth=int(math.sqrt(len(kernel)))
    khight=int(math.sqrt(len(kernel)))
    change=int((kwidth-1)/2 )
    kx=change
    ky=change
    #this basically gives center of kernel
    
    def get_kernel(kernel, x, y):
        return kernel[(y)*kwidth+(x)]
    
    def get_pixel_kernel(image,x,y):
        if x<0:
            x=0
        if x>image['width']-1:
            x=image['width']-1
        if y<0:
            y=0
        if y>image['height']-1:
            y=image['height']-1
        return image['pixels'][(y)*(image['width'])+(x)]
    
    def apply_kernel(kernel, image,x,y):
        new=0
        for kery in range(khight):
            for kerx in range(kwidth):
                ydiff=ky-kery
                xdiff=kx-kerx
                
                pixel=get_pixel_kernel(image, int(x-xdiff), int(y-ydiff))
                
                kernelvalue=get_kernel(kernel,kerx,kery)
                new+=pixel*kernelvalue
                
        return new

    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    for y in range(image['height']):
        for x in range(image['width']):
            pixel=apply_kernel(kernel,image,x,y)
            result['pixels'].append(pixel)
    return result
            



def round_and_clip_image(image):
 
    for index in range(len(image['pixels'])):
        if image['pixels'][index]<0:
            image['pixels'][index]=0
        if image['pixels'][index]>255:
            image['pixels'][index]=255
    for index in range(len(image['pixels'])):
        image['pixels'][index]=round(image['pixels'][index])
    return image
    
# FILTERS


        
def edges(image):
    kernelx=[-1, 0, 1,
-2, 0, 2,
-1, 0, 1]
    kernely=[-1, -2, -1,
 0,  0,  0,
 1,  2,  1]
    first=correlate(image, kernelx)
    second=correlate(image, kernely)
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    for pos in range(len(image["pixels"])):
        x=first["pixels"][pos]
        y=second['pixels'][pos]
        pixel=math.sqrt(x**2+y**2)
        result['pixels'].append(pixel)
    newim=round_and_clip_image(result)
    
    return newim   

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
  
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}
    
def save_greyscale_image(image, filename, mode='PNG'):
    
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()

 #SEAM CARVING

 #Main Seam Carving Implementation

def seam_carving(image, ncols):
   
    imagecopy={'height': image['height'],'width': image['width'],'pixels': image['pixels'].copy()}
    
    minimumindex=[]
    for col in range(ncols):
        #we iterate and apply all the helper functions ncol times.
        grey=greyscale_image_from_color_image(imagecopy)
        energy=compute_energy(grey)
        c=cumulative_energy_map(energy)
        minimum=minimum_energy_seam(c)
        minimumindex.append(minimum)
        imagecopy=image_without_seam(imagecopy, minimum)

    return imagecopy,minimumindex

# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
   
    #this creates a new dictionary
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    #by going through every pixel and then combining the tuple values, we can get pixel with one value
    for pixel in image['pixels']:
        r=pixel[0]
        g=pixel[1]
        b=pixel[2]
        v=round(.299*r+.587*g+.114*b)
        result['pixels'].append(v)
    return result
    


def compute_energy(grey):
    
    energypic=edges(grey)
    
    return energypic  


def cumulative_energy_map(energy):
    
    def get_pixel(image, x, y):
        return image['pixels'][(y)*(image['width'])+(x)]
    
    def get_pixel_energy(image,x,y):
        #this helper function allows us to get pixel value and if it is out of bounds 
        #then we use the pixel value right next to it and for first row return 0
        if x<0:
            x=0
        if x>image['width']-1:
            x=image['width']-1
        if y<0:
            return 0
        else:
            
            return image['pixels'][(y)*(image['width'])+(x)]
        
    result = {
        'height': energy['height'],
        'width': energy['width'],
        'pixels': [],
    }
    
    for y in range(energy['height']):
        for x in range(energy['width']):
            #iterate through every pixel and finds the min of the three pixels above and adds to cum
            prior3=[]
            prior3.append(get_pixel_energy(result,x-1,y-1))
            prior3.append(get_pixel_energy(result,x,y-1))
            prior3.append(get_pixel_energy(result,x+1,y-1))
            
            cumenergypixel=get_pixel(energy,x,y)+min(prior3)
            result['pixels'].append(cumenergypixel)
            
    return result
    


def minimum_energy_seam(c):
    
    def get_pixel(image, x, y):
       
        return image['pixels'][(y)*(image['width'])+(x)]
    #list of indices from bottom up
    indices=[]
    
    #botton row has postition y=height-1
    #this finds the smallest pixel in botton row
    y=c['height']-1
    initvalue=get_pixel(c,0,y)
    xposition=0
    for x in range(c['width']):
        if get_pixel(c,x,y)<initvalue:
            xposition=x
            initvalue=get_pixel(c,xposition,y)

    indices.append((xposition,y))
    
    #goes through rows from bottom up
    for yvalue in range(2,c['height']+1):
        y=c['height']-yvalue
        #creates a new list and appends the three values before the pixel
        lst=[]
        
        #this for loop goes through the three pixels before the curent pixel and finds the smallest
        for xpos in (xposition-1,xposition, xposition+1):
            if xpos<0 or xpos>c['width']-1:
                lst.append(float('inf')) 
            else:
                lst.append(get_pixel(c,xpos,y))
            small=min(lst)
       
        
        #This for loop goes through the three pixels again to obtain the position of the pixel
        for xpos in (xposition-1,xposition, xposition+1):
            if xpos<0 or xpos>c['width']-1:
                pass
            elif get_pixel(c,xpos,y)==small:
                xposition=xpos
                break
                
        if (xposition,y) not in indices:
            indices.append((xposition,y))
  
    return (indices)
        


def image_without_seam(im, s):
    
    result = {
        'height': im['height'],
        'width': im['width']-1,
        'pixels': [],
    }
    #iterates through every pixel and only adds to new image if the pixel is not in s
    for y in range(im['height']):
        for x in range(im['width']):
            if (x,y) not in s:
                result['pixels'].append(get_pixel(im,x,y))
            # else:
            #      result['pixels'].append((255,0,0))
    
    return result


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()
    
    # HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_image(filename):
    
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    
    
    image=load_color_image('image')
    newim=seam_carving(image, 100)
    save_color_image(newim,'image.png')
    
