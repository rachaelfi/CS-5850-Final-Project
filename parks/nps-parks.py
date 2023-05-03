import requests as rq
import json
import pandas as pd


state = "ut"
KEY = "HZxd2uuNWcWSsvZU0ESQhlvVZqqodlWDjeTVhfIc"
url = "https://developer.nps.gov/api/v1/parks?stateCode=" + state +"&api_key=" + KEY

response = rq.get(url)

data = response.json()
data = data['data']

pname = []
plat = []
plng = []

for park in data:
    pname.append(park['fullName'])
    plat.append(park['latitude'])
    plng.append(park['longitude'])

df = pd.DataFrame()
df['name'] = pname
df['latitude'] = plat
df['longitude'] = plng

df = df[['name','latitude', 'longitude']]

df.to_csv('nps-parks.csv', sep=',')