import requests as rq
import json
import pandas as pd


# This takes a minute to run

url = "https://www.churchofjesuschrist.org/temples/list?lang=eng"

response = rq.get(url)
sub_res = str(response.content)
sub_res = sub_res[sub_res.find("templeList"):]
sub_res = sub_res[:sub_res.find("],")]
sub_res = '{"' + sub_res + "]}"
sub_res = sub_res.replace("\\", "\\\\")

subAsJson = json.loads(sub_res)
subAsJson = subAsJson["templeList"]

utahTemples = []
for temple in subAsJson:
    if temple["stateRegion"] == " Utah":
        utahTemples.append(temple['templeNameId'])

detailsURL = "https://www.churchofjesuschrist.org/temples/details/"
langHeader = "?lang=eng"

adr = []

for templeId in utahTemples:
    detailsURLComplete = detailsURL + templeId + langHeader
    res = rq.get(detailsURLComplete)
    res = str(res.content)
    res = res[res.find('"details"'):]
    res = "{" + res[:res.find(',"mapText"')] + "}]}"

    resJson = json.loads(res)
    resJson = resJson['details'][0]
    print(resJson)
    adr.append(resJson['addLine1'] + " " + resJson['addLine2'] + " " + resJson['addLine3'])

df = pd.DataFrame()

df['templeId'] = utahTemples
df['address'] = adr

df['templeId'] = df['templeId'].astype('str')
df['address'] = df['address'].astype('str')
df = df[['templeId', 'address']]
df.to_csv('temples.csv', sep='\t')