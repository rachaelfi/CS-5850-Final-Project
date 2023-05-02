import requests as rq
import json


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

print(plat)