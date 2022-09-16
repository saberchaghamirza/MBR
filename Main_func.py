# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:58:05 2022

@author: saber
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon
import pandas as pd
import matplotlib
matplotlib.use('QtAgg')
from Parcel_Properties import Properties
from pandasql import sqldf
import matplotlib.pyplot as plt
from MBR import rotation,difference_from_rec
mysql = lambda q: sqldf(q, globals()) 


shapfile_address=r'D:\Projects\bulding_aproxmate\footprintSample\raw01.shp'
i=460
lands=gpd.read_file(shapfile_address)

# start
polygon=Polygon(lands.geometry[i])
land = gpd.GeoDataFrame(geometry=[polygon])
Properties= Properties(land)


# make the ploygon ready for simplyfiy
land=lands.geometry[i]
points_all=list(land.exterior.coords)
polygon=Polygon(lands.geometry[i])   
land = gpd.GeoDataFrame(geometry=[polygon])

# MBR
t=0.8
finall_land = gpd.GeoDataFrame(geometry=[])

ready_land=rotation(land)
finall_land=difference_from_rec(ready_land,t)
area=10
# difference
while area>1:
    ready_land=ready_land.difference(finall_land)
    mbr_land=difference_from_rec(ready_land,t)
    area=mbr_land.dissolve().area
    finall_land = gpd.GeoDataFrame( pd.concat( [finall_land,mbr_land], ignore_index=True,sort=False) )
# show
fig, ax = plt.subplots(1,1)
mbr_land = gpd.GeoDataFrame(geometry=[mbr_land.geometry[0]])
finall_land.plot(ax=ax,edgecolor='black',color='white',linewidth=0.5)

# read the file 
