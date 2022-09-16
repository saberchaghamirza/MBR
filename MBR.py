# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 10:51:18 2022

@author: Saber
"""
from math import pi,atan2
from line_segment import line_segment

def rotation(land):
    all_lines=line_segment(land)
    longest=0
    for geos in all_lines.geometry:
            if geos.length>longest:
                longest=geos.length
                line=geos
    x1=line.coords[0][0]
    y1=line.coords[0][1]
    x2=line.coords[1][0]
    y2=line.coords[1][1]
    slop=atan2((y2-y1),(x2-x1))
    slop=slop*180/pi
    ready_land=land.rotate(slop)
    
    return ready_land

import geopandas as gpd
import pandas as pd

def difference_from_rec(parcel,t):
    rec_big=parcel.envelope
    # difference
    difference=rec_big.difference(parcel)
    difference = gpd.GeoDataFrame(geometry=[difference.geometry[0]])
    difference=difference.dissolve()
    difference=difference.explode(ignore_index=True)
    finall_rec = gpd.GeoDataFrame(geometry=[])
    mbr_land=rec_big
       # extract polygons out of multipolygon
    for geo in difference.geometry:
        rec = gpd.GeoDataFrame(geometry=[geo])
        rec=rec.envelope
        rec = gpd.GeoDataFrame(geometry=[rec.geometry[0]])
        finall_rec = gpd.GeoDataFrame( pd.concat( [finall_rec,rec], ignore_index=True,sort=False) )
        if float(rec.area)>t:
         mbr_land=mbr_land.difference(rec)
        
    mbr_land = gpd.GeoDataFrame(geometry=[mbr_land.geometry[0]])
    return mbr_land


