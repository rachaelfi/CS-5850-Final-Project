import pandas as pd
import requests
import csv
import sys

API_KEY = ""

url_base = 'https://maps.googleapis.com/maps/api/geocode/json?address='


df = pd.read_csv('../Data/zillow.csv')

for index, home in df.iterrows():
    address = home['Address']
    address = address.replace(" ", "+")
    address = address.replace("#", "")
    url = url_base + address + "&key=" + API_KEY

    response = requests.get(url).json()
    if response['results'] == []:
        continue
    latlong = response['results'][0]['geometry']['location']
    df.at[index, 'Latitude'] = latlong['lat']
    df.at[index, 'Longitude'] = latlong['lng']
    print("updated: " + str(index))
    

df.to_csv("../Data/zillow2.csv", sep=',')


# response = requests.get(url).json()
# print(response['results'][0]['geometry']['location'])
