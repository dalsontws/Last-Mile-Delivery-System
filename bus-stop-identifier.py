#!/usr/bin/env python
# coding: utf-8

import os, time, datetime, sys, json, glob
import datetime
import pandas as pd
import numpy as np
import os

# Make a GET request to compare delivery locations with your chosen bus stops
import requests 

file2 = "datasets-dodo/clean/bus_stop.xlsx"

df2 = pd.read_excel(file2)


# Add your specific pick up and delivery locations, to identify best bus stop.
pickupLat = '50.0677682'
pickupLong = '14.4680777'

deliverLat = '50.0541071'
deliverLong = '14.5036845'
minTime = 1000000

for index, row in df2.iterrows():
    stopLat = row['latitude']
    stopLong = row['longitude']
    stopName = row['stop']

    payload1 = {'app_id':'YOUR APP ID',
               'app_code':'YOUR APP CODE',
               'waypoint0':'geo!' + str(pickupLat) + ',' + str(pickupLong),
               'waypoint1':'geo!' + str(stopLat) + ',' + str(stopLong),
               'mode':'fastest;car;traffic:enabled' }
    response1 = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload1)

    payload2 = {'app_id':'YOUR APP ID',
               'app_code':'YOUR APP CODE',
               'waypoint0':'geo!' + str(stopLat) + ',' + str(stopLong),
               'waypoint1':'geo!' + str(deliverLat) + ',' + str(deliverLong),
               'mode':'fastest;bicycle' }
    response2 = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload2)

    # get json, print summary
    route1 = response1.json()
    route2 = response2.json()
    distance1 = route1['response']['route'][0]['summary']['distance'] + route2['response']['route'][0]['summary']['distance']
    travelTime1 = route['response']['route'][0]['summary']['travelTime'] + route2['response']['route'][0]['summary']['travelTime']

    if (travelTime1 < minTime):
        minTime = travelTime1
        lat = stopLat
        long = stopLong
        name = stopName


    print("Distance: " + str(distance1/1000) + "km Travel Time: " + str(travelTime1/60.0) + "min")

print("Stop is: " + name)


