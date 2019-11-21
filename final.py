#!/usr/bin/env python
# coding: utf-8

import os, time, datetime, sys, json, glob
import datetime
import pandas as pd
import numpy as np
import os

dir = "datasets-dodo/delivery_data.csv"


df = pd.read_csv(dir, sep=';')

# Choose your pick up address here
df = df.loc[df['pickup_address'] == 'Plzeň, Sukova 2895/23']

# Choose your delivery date
df = df.loc[df['required_delivery'].str.contains('2017-02-16')]

df['pickup_latitude'] = df['pickup_latitude'].astype(str)
df['pickup_longitude'] = df['pickup_longitude'].astype(str)
df['delivery_latitude'] = df['delivery_latitude'].astype(str)
df['delivery_longitude'] = df['delivery_longitude'].astype(str)

#Used to check validity
#df.head()


from decimal import *

df = pd.read_csv(dir, sep=';')


# df = df.loc[df['pickup_address'] == 'Plzeň, Sukova 2895/23']
# df = df.loc[df['pickup_address'] == 'Praha, U Slavie 1527']
df = df.dropna()
df = df.loc[df['required_delivery'].str.contains('2018')]


# df['pickup_latitude'] = df['pickup_latitude'].astype(str)
# df['pickup_longitude'] = df['pickup_longitude'].astype(str)
# df['delivery_latitude'] = df['delivery_latitude'].astype(str)
# df['delivery_longitude'] = df['delivery_longitude'].astype(str)

df[['pickup_latitude', 'pickup_longitude']] = df[['pickup_latitude', 'pickup_longitude']].astype(str)
df[['delivery_latitude', 'delivery_longitude']] = df[['delivery_latitude', 'delivery_longitude']].astype(str)
df[['created', 'required_delivery', 'delivered']] = df[['created', 'required_delivery', 'delivered']].astype(str)

df['required_delivery'] =  pd.to_datetime(df['required_delivery'])
df['created'] =  pd.to_datetime(df['created'])
df['delivered'] =  pd.to_datetime(df['delivered'])

df['pickup_latitude'] = df['pickup_latitude'].str.replace(',', '')
df['pickup_longitude'] = df['pickup_longitude'].str.replace(',', '')

df['delivery_latitude'] = df['delivery_latitude'].str.replace(',', '')
df['delivery_longitude'] = df['delivery_longitude'].str.replace(',', '')


# df['delivery_latitude'] = pd.to_numeric(df['delivery_latitude'], downcast='float')
# df['delivery_longitude'] = pd.to_numeric(df['delivery_longitude'], downcast='float')



# remove after, can be better 
# df['delivery_latitude'] = df['delivery_latitude'].apply(Decimal)
# df['delivery_longitude'] = df['delivery_longitude'].apply(Decimal)

df['pickup_latitude'] = (df['pickup_latitude'].str[:2] + '.' + df['pickup_latitude'].str[2:]).astype(float)
df['pickup_longitude'] = (df['pickup_longitude'].str[:2] + '.' + df['pickup_longitude'].str[2:]).astype(float)

df['delivery_latitude'] = (df['delivery_latitude'].str[:2] + '.' + df['delivery_latitude'].str[2:]).astype(float)
df['delivery_longitude'] = (df['delivery_longitude'].str[:2] + '.' + df['delivery_longitude'].str[2:]).astype(float)

# df['delivery_latitude'] = decimal.Decimal(df['delivery_latitude']).adjusted() - 1
# df['delivery_longitude'] = decimal.Decimal(df['delivery_longitude']).adjusted() - 1


# df_filtered = df[df['required_delivery'] < df['delivered']]

# df = df.drop(df[df['required_delivery'] < df['delivered']].index, axis=0)


df = df[['order_id','pickup_address', 'pickup_latitude', 'pickup_longitude', 'delivery_latitude', 'delivery_longitude', 'created', 'delivered', 'required_delivery', 'courier_id']]

# df.head()


# print(df.shape)

df.to_excel("E:/Skoda/datasets/clean/delivery_data_2018.xlsx")
# df_filtered.to_csv("E:/Skoda/datasets/clean/delivery_data_april2019_late.csv")


# In[3]:


# Make a get request to get the latest position of the international space station from the opennotify api.
import requests 

file1 = "datasets-dodo/clean/delivery_data_491_398_.xlsx"
file2 = "datasets-dodo/clean/bus_stop.xlsx"

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

totalDist = 0
totalTime = 0
count = 0

for index, row in df1.iterrows():
    pickupLat = row['pickup_latitude'] 
    pickupLong = row['pickup_longitude']
    deliverLat = row['delivery_latitude'] 
    deliverLong = row['delivery_longitude']
    courierID = row['courier_id']

    payload = {'app_id':'c98RVLVhTMmpsKrlP3lH', 
               'app_code':'SOZSIt6MOtk_5TDi5K6C5Q', 
               'waypoint0':'geo!' + str(pickupLat) + ',' + str(pickupLong), 
               'waypoint1':'geo!' + str(deliverLat) + ',' + str(deliverLong), 
               'mode':'fastest;car;traffic:enabled' }
    response = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload)

    # get json, print summary
    route = response.json()
#     print(type(route))
#     print (route)
    distance = route['response']['route'][0]['summary']['distance']
    travelTime= route['response']['route'][0]['summary']['travelTime']
    
    if (distance >= 2.2*1000):
#         checkRoute(pickupLat, pickupLong, deliverLat, deliverLong)  
        file2 = "datasets-dodo/clean/bus_stop.xlsx"

        df2 = pd.read_excel(file2)

        minTime = 1000000

        for index, row in df2.iterrows():
            stopLat = row['latitude'] 
            stopLong = row['longitude']
            stopName = row['stop']
    
            payload1 = {'app_id':'c98RVLVhTMmpsKrlP3lH', 
                   'app_code':'SOZSIt6MOtk_5TDi5K6C5Q', 
                   'waypoint0':'geo!' + str(pickupLat) + ',' + str(pickupLong), 
                   'waypoint1':'geo!' + str(stopLat) + ',' + str(stopLong), 
                   'mode':'fastest;car;traffic:enabled' }
            response1 = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload1)
    
            payload2 = {'app_id':'c98RVLVhTMmpsKrlP3lH', 
                   'app_code':'SOZSIt6MOtk_5TDi5K6C5Q', 
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
                dist = distance1
                minTime = travelTime1 
                lat = stopLat
                long = stopLong
                name = stopName
        
        
            print("Distance(drive + cycle): " + str(distance1/1000) + 
                  "km Travel Time(drive + cycle): " + str(travelTime1/60.0) + "min")

        print("Stop is: " + name)
        print("\n")
        
        
    totalDist += distance
    totalTime += travelTime
    
    

    print("Distance: " + str(distance/1000) + "km Travel Time: " + str(travelTime/60.0) + 
          "min" + ', delivered by ' + str(courierID))
    print("\n")

totalDist *= 2
totalDist /=1000
totalTime *= 2
totalTime /= 60.0

# print("Total Distance: " + str(totalDist) + "km Total Travel Time: " + str(totalTime) + "min")
# print("\n")


# def checkRoute(pickupLat, pickupLong, deliverLat, deliverLong):
#     file2 = "E:/Skoda/datasets/clean/bus_stop.xlsx"

#     df2 = pd.read_excel(file2)

#     minTime = 1000000

#     for index, row in df2.iterrows():
#         stopLat = row['latitude'] 
#         stopLong = row['longitude']
#         stopName = row['stop']
    
#         payload1 = {'app_id':'c98RVLVhTMmpsKrlP3lH', 
#                'app_code':'SOZSIt6MOtk_5TDi5K6C5Q', 
#                'waypoint0':'geo!' + str(pickupLat) + ',' + str(pickupLong), 
#                'waypoint1':'geo!' + str(stopLat) + ',' + str(stopLong), 
#                'mode':'fastest;car;traffic:enabled' }
#         response1 = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload1)
    
#         payload2 = {'app_id':'c98RVLVhTMmpsKrlP3lH', 
#                'app_code':'SOZSIt6MOtk_5TDi5K6C5Q', 
#                'waypoint0':'geo!' + str(stopLat) + ',' + str(stopLong), 
#                'waypoint1':'geo!' + str(deliverLat) + ',' + str(deliverLong), 
#                'mode':'fastest;bicycle' }
#         response2 = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload2)

#         # get json, print summary
#         route1 = response1.json()
#         route2 = response2.json()
#         distance1 = route1['response']['route'][0]['summary']['distance'] + route2['response']['route'][0]['summary']['distance']
#         travelTime1 = route['response']['route'][0]['summary']['travelTime'] + route2['response']['route'][0]['summary']['travelTime'] 
    
#         if (travelTime1 < minTime):
#             dist = distance1
#             minTime = travelTime1 
#             lat = stopLat
#             long = stopLong
#             name = stopName
        
        
#         print("Distance(drive + cycle): " + str(distance1/1000) + 
#               "km Travel Time(drive + cycle): " + str(travelTime1/60.0) + "min")

#     print("Stop is: " + name)
#     print("\n")



# for key, value in route.items():
#     if key is 'summary': #'name' is the key we wish to get the value from
#         print(value) # print its value
        
        
# print(route["response"]["route"]["summary"]['text'])



# Print the status code of the response.
# print(response.text("summary"))



# In[132]:


file = "E:/Skoda/datasets/clean/delivery_data_april_jizni.xlsx"

df1 = pd.read_excel(file)

sumX = 0.0
sumY = 0.0

for index, row in df1.iterrows():
    x = row['delivery_latitude']
    y = row['delivery_longitude']
    sumX += x
    sumY += y
    
numRows = len(df1) 

centroid = (sumX / numRows, sumY / numRows)
print(centroid, numRows)


# In[185]:





# In[192]:


file2 = "E:/Skoda/datasets/clean/bus_stop.xlsx"

df2 = pd.read_excel(file2)


pickupLat = '50.0677682'
pickupLong = '14.4680777'

deliverLat = '50.0541071'
deliverLong = '14.5036845'
minTime = 1000000

for index, row in df2.iterrows():
    stopLat = row['latitude'] 
    stopLong = row['longitude']
    stopName = row['stop']
    
    payload1 = {'app_id':'c98RVLVhTMmpsKrlP3lH', 
               'app_code':'SOZSIt6MOtk_5TDi5K6C5Q', 
               'waypoint0':'geo!' + str(pickupLat) + ',' + str(pickupLong), 
               'waypoint1':'geo!' + str(stopLat) + ',' + str(stopLong), 
               'mode':'fastest;car;traffic:enabled' }
    response1 = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload1)
    
    payload2 = {'app_id':'c98RVLVhTMmpsKrlP3lH', 
               'app_code':'SOZSIt6MOtk_5TDi5K6C5Q', 
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


# payload = {'app_id':'c98RVLVhTMmpsKrlP3lH', 
#             'app_code':'SOZSIt6MOtk_5TDi5K6C5Q', 
#             'waypoint0':'geo!' + str(pickupLat) + ',' + str(pickupLong), 
#             'waypoint1':'geo!' + str(lat) + ',' + str(long), 
#             'mode':'fastest;car;traffic:enabled' }
# response = requests.get('https://route.api.here.com/routing/7.2/calculateroute.json', params=payload)

# # get json, print summary
# route = response.json()
# distance2 = route['response']['route'][0]['summary']['distance']
# travelTime2 = route['response']['route'][0]['summary']['travelTime']

# print("Distance: " + str(distance2/1000) + "km Travel Time: " + str(travelTime2/60.0) + "min")


# In[ ]:




