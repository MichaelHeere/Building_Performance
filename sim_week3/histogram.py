# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:28:40 2021

@author: Michaël
"""

import matplotlib.pyplot as plt
import numpy as np

buildingheight = [
    [0, 517000],
    [10, 123000],
    [20, 6100],
    [30, 1915],
    [40, 616],
    [50, 281],
    [60, 191],
    [70, 73],
    [80, 26],
    [90, 17],
    [100, 37]]

heights = {}
heightindex = []
heightvalue = []

for i in range(len(buildingheight)):
    heights[buildingheight[i][0]] = buildingheight[i][1]
    heightindex.append(buildingheight[i][0])
    heightvalue.append(buildingheight[i][1])
    
    
SMALL_SIZE = 16
MEDIUM_SIZE = 16
BIGGER_SIZE = 22

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


hh2 = plt.hist(heightindex, weights = heightvalue, log=True, histtype='stepfilled')
plt.ylabel('Number of buildings')
plt.xlabel('Height')
plt.savefig('barplot.png')



#hh1 = plt.hist(heights.keys(), weights=heights.values(), label="counted_data")
