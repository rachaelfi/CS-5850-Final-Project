import requests as rq
import json


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

templesWithAddresses = {}

for templeId in utahTemples:
    detailsURLComplete = detailsURL + templeId + langHeader
    res = rq.get(detailsURLComplete)
    res = str(res.content)
    res = res[res.find('"details"'):]
    res = "{" + res[:res.find(',"mapText"')] + "}]}"
    print('"' + templeId + '": ' + res)
    templesWithAddresses[templeId] = res


print(templesWithAddresses)