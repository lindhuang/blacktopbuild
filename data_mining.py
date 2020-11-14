# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
# CR = crash report
CR = pd.read_csv(r"C:\Users\lcpap\OneDrive\Documents\Blacktop Build\Crash_Report.csv");

# this is a list of numerical dates that can be used to compare to the crash dates to see overlap
CR_dates = CR.dispatch_ts;

#variable to store the rain dates for comparison
CR_dates_2 = [];
for d in CR_dates:
    x = d[0:4]+d[5:7]+d[8:10];
    CR_dates_2.append(x); 

total_crashes = len(CR_dates_2);
print("The total number of crashes is ", total_crashes);

#WD = weather data
WD = pd.read_csv(r"C:\Users\lcpap\OneDrive\Documents\Blacktop Build\Boston_Weather_Data.csv");

#print(WD);
rainy_days = WD[WD['Basel Precipitation Total']>0]; 

# this is a list of numerical dates that can be used to compare to the crash dates to see overlap
rain_dates = rainy_days.timestamp;

#variable to store the rain dates for comparison
rain_dates_2 = [];

for d in rain_dates:
    rain_dates_2.append(d[0:8]);        

print("Rainy days length", len(rain_dates_2));
print("Total Days:", len(WD))

snow_days = WD[WD['Basel Snowfall Amount']>0];
#print(snow_days);

# this is a list of numerical dates that can be used to compare to the crash dates to see overlap
snow_dates = snow_days.timestamp;

#variable to store the snow dates for comparison
snow_dates_2 = [];

for d in snow_dates:
    snow_dates_2.append(d[0:8]); 

#print("Snow days length", len(snow_dates_2));    
    
#calculate the number of crashes on rainy days
rainy_day_crashes = 0;
for i in CR_dates_2:
    if i in rain_dates_2:
        rainy_day_crashes= rainy_day_crashes+1;
        
print("The number of crashes on a rainy day is ", rainy_day_crashes);

print("The percentage of crashes on a rainy day is: ", (rainy_day_crashes/total_crashes)*100);

#calculate the number of crashes on snowy days
snow_day_crashes = 0;
for i in CR_dates_2:
    if i in snow_dates_2:
        snow_day_crashes= snow_day_crashes+1;
        
print("The number of crashes on a snowy day is ", snow_day_crashes);

print("The percentage of crashes on a snowy day is: ", (snow_day_crashes/total_crashes)*100);


# calculate percentage motor crashes
mv = CR[CR['mode_type']=="mv"];
num_mv_crashes = len(mv);
print("Number of Motor Vehicle crashes", num_mv_crashes);
print("The percentage motor vehicle: ", (num_mv_crashes/total_crashes)*100);

# calculate percentage ped crashes
ped = CR[CR['mode_type']=="ped"];
num_ped_crashes = len(ped);
print("Number of Pedestrian crashes", num_ped_crashes);
print("The percentage pedestrian: ", (num_ped_crashes/total_crashes)*100);

# calculate percentage motor crashes
bike = CR[CR['mode_type']=="bike"];
num_bike_crashes = len(bike);
print("Number of bike crashes", num_bike_crashes);
print("The percentage bike ", (num_bike_crashes/total_crashes)*100);

# filtering by location type 
intersections = CR[CR['location_type']=="Intersection"];
num_intersection_crashes = len(intersections);
print("Number of intersection crashes", num_intersection_crashes);
print("The percentage of crashes at intersections is: ", (num_intersection_crashes/total_crashes)*100);

street = CR[CR['location_type']=="Street"];
num_street_crashes = len(street);
print("Number of street crashes", num_street_crashes);
print("The percentage of crashes on streets is: ", (num_street_crashes/total_crashes)*100);

other = CR[CR['location_type']=="Other"];
num_other_crashes = len(other);
print("Number of other crashes", num_other_crashes);
print("The percentage of other crashes: ", (num_other_crashes/total_crashes)*100);








    