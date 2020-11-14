from math import acos,cos,sin,pi,atan2
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import requests
from shapely.geometry import Point, Polygon

def great_circle_distance(loc1, loc2):
    """
    Returns the approximate distance between (lat1, lon1) and (lat2, lon2) in
    miles, taking into account the Earth's curvature (but assuming a spherical
    earth).

    Latitude and longitudes given in degrees.  Thanks to Berthold Horn for this
    implementation.
    """
    lat1, lon1 = loc1
    lat2, lon2 = loc2
    phi1 = lat1*pi/180.
    theta1 = lon1*pi/180.
    phi2 = lat2*pi/180.
    theta2 = lon2*pi/180.
    cospsi = sin(phi1)*sin(phi2) + cos(phi1)*cos(phi2)*cos(theta2-theta1)
    sinpsi = ((sin(theta1)*cos(phi1)*sin(phi2) - sin(theta2)*cos(phi2)*sin(phi1))**2 +\
              (cos(theta2)*cos(phi2)*sin(phi1) - cos(theta1)*cos(phi1)*sin(phi2))**2 +\
              (cos(phi1)*cos(phi2)*sin(theta2-theta1))**2)**0.5
    return atan2(sinpsi,cospsi) * 3958


def get_boston_crash_data():
    url = 'https://data.boston.gov/api/3/action/datastore_search?resource_id=e4bfe397-6bfc-49c5-9367-c879fac7401d&limit=24523'

    response = (requests.get(url)).json()

    results = response['result']['records']
    # convert response['result']['records'] to df
    #cols = results[0].keys()

    # 24523 elements
    df = pd.DataFrame(results)

    # 11959 elements
    # filter for intersections
    df_intersections = df[df['location_type'] == 'Intersection'].reset_index()

    geo_df = gpd.GeoDataFrame(
        df_intersections, geometry=gpd.points_from_xy(df_intersections.long, df_intersections.lat))

    sub_geo_df = geo_df.head(200)

    # Get shape file for Boston
    url_geo = 'https://opendata.arcgis.com/datasets/cfd1740c2e4b49389f47a9ce2dd236cc_8.geojson'
    boston_boundaries = gpd.read_file(url_geo)

    # Plot map of boston with 200 crashes also plotted
    fig, ax = plt.subplots(figsize=(20, 20))
    boston_boundaries.plot(ax=ax, alpha=0.4, color="grey", edgecolor='black')
    sub_geo_df.plot(ax=ax, markersize=25, alpha=0.8, color="r", marker='x', label='crashes')

    return boston_boundaries, df_intersections


def get_clusters(df_intersections, threshold=25):

    # Create clusters of crashes
    # have a seen index
    # index is lat and long point, value is a list of indices from the df
    clusters = {}

    for index, row in df_intersections.iterrows():
        # round to 4 decimals, if not in clusters
        # check if in clusters - 4 decimals points finds intersections within 0.01 miles
        lat = round(float(row['lat']), 4)
        lon = round(float(row['long']), 4)

        if (lat, lon) in clusters:
            clusters[(lat, lon)].append(row['index'])

        else:
            clusters[(lat, lon)] = [row['index']]

    # make a new dataframe per cluster, plot in different colors
    # remove clusters with only one or two accidents there
    #threshold = 25

    clusters_compact = {}
    for k, v in clusters.items():
        if len(v) > threshold:
            clusters_compact[k] = v

    return clusters_compact


def clusters_to_csv(clusters_comapct):

    count_clusters = {'latitude': [], 'longitude': [], 'num crashes': []}
    for k, v in clusters_comapct.items():
        count_clusters['latitude'].append(k[0])
        count_clusters['longitude'].append(k[1])
        count_clusters['num crashes'].append(len(v))

    clusters_df = pd.DataFrame(count_clusters)
    # print(clusters_df)
    clusters_df.to_csv('clusters.csv')


def plot_clusters(boston_boundaries, clusters_compact, df_intersections):
    fig, ax = plt.subplots(figsize=(20, 20))
    boston_boundaries.plot(ax=ax, alpha=0.4, color="grey", edgecolor='black')

    for k, v in clusters_compact.items():
        frames = []
        for i in v:
            frames.append(df_intersections[df_intersections['index'] == i])

        df = pd.concat(frames)
        df.reset_index()

        geo_df_cluster = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df.long, df.lat))
        # print(df)
        geo_df_cluster.plot(ax=ax, markersize=25, alpha=0.8, color="r", marker='x', label='crashes')
