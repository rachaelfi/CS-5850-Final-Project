import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import csv 
import json
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import regex as re
import requests
import lxml
from lxml.html.soupparser import fromstring
import prettify
import numbers
import htmltext

request_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


with requests.Session() as session:
    zip = '84401'
    url = 'https://www.zillow.com/homes/for_sale/' + zip
    response = session.get(url, headers=request_headers)
    soup = BeautifulSoup(response.content, 'lxml')
    # soup1 = BeautifulSoup(response.content, 'html.parser')
    # soup2 = BeautifulSoup(response.content, 'html.parser')
    # soup3 = BeautifulSoup(response.content, 'html.parser')
    # soup4 = BeautifulSoup(response.content, 'html.parser')
    df = pd.DataFrame()
    df1 = pd.DataFrame()

    address = soup.find_all ('address', {'data-test':'property-card-addr'})
    price = soup.find_all('span', {'data-test':'property-card-price'})
    seller = soup.find_all('div', {'class':'cWiizR'})

    adr=[]
    pr=[]
    sl=[]
    for result in address:
        adr.append(result.text)
    for result in price:
        pr.append(result.text)
    for result in seller:
        sl.append(result.text)
    
    df['seller'] = sl
    df['address'] = adr
    df['prices'] = pr
    
    df['seller'] = df['seller'].astype('str')
    df['prices'] = df['prices'].astype('str')
    df['address'] = df['address'].astype('str')

    df = df[['prices', 'address', 'seller']]
    print(df)
    df.to_csv('zillow.csv', sep='\t')

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
          'referer':'https://www.zillow.com/homes/Missoula,-MT_rb/'}



# data = requests.get('https://www.zillow.com/ut/', headers=header)
# soup = BeautifulSoup(data.text, 'lxml')

# address = soup.find_all('address', {'data-test':'property-card-addr'})
# price = soup.find_all('span', {'data-test':'property-card-price'})
# seller =soup.find_all('div', {'class':'cWiizR'})


adr=[]
pr=[]
sqr=[]
# lat=[]
# long=[]


with open('zillow.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Address', 'Price', 'Square Feet', 'Latitude', 'Longitude']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for page in range(1, 21):
        url = f'https://www.zillow.com/ut/{page}_p/'
        data = requests.get(url, headers=header)
        soup = BeautifulSoup(data.text, 'lxml')

        for result in soup.find_all('ul', {'class': 'dmDolk'}):
            li_list = result.find_all('li')
            if len(li_list) > 1:
                sqr.append(li_list[2].text)
            else:
                sqr.append('N/A')
        # Address
        for result in soup.find_all('address', {'data-test':'property-card-addr'}):
            adr.append(result.text)
        # Price
        for result in soup.find_all('span', {'data-test':'property-card-price'}):
            pr.append(result.text)
            
        # Lat and Long 
        # for result in soup.find_all('li', {'class': 'jhnswL'}):
        #     json_data = None
        #     for script in result.find_all('script', {'type': 'application/ld+json'}):
        #         if 'geo' in script.text:
        #             json_data = json.loads(script.text)
        #             break
        #         if json_data:
        #             lat.append(json_data['geo']['latitude'])
        #             long.append(json_data['geo']['longitude'])
        #         else:
        #             lat.append('N/A')
        #             long.append('N/A')
        # for result in soup.find_all('li', {'class': 'jhnswL'}):
        #     for item in result.find_all('script', {'type': 'application/ld+json'}):
        #         if item is None:
        #             lat.append('N/A')
        #             long.append('N/A')
        #         else:
        #             json_data = json.loads(item.text)
        #             lat.append(json_data['geo']['latitude'])
        #             long.append(json_data['geo']['longitude'])
                    
        #         print(lat)
                
        
            
    for i in range(len(adr)):
        if i < len(sqr):
            writer.writerow({'Address': adr[i],
                        'Price': pr[i],
                        'Square Feet': sqr[i],
                        # 'Latitude': lat[i],
                        # 'Longitude': long[i]
                        })
            # print("I made it here")
        else:
            writer.writerow({'Address': adr[i],
                        'Price': pr[i],
                        'Square Feet': 'N/A'})
        

print(adr)
print(pr)
print(sqr)
# print(lat)
# print(long)



# DRIVER_PATH = 'C:\chromedriver.exe' 
# service = Service(DRIVER_PATH)
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
# # driver = webdriver.Chrome(service=service)
# driver.get('https://www.zillow.com/portland-or/')

# time.sleep(10)#To help window stay open

# address = driver.find_elements(By.XPATH,'//address')
# price = driver.find_elements(By.XPATH,'//article/div/div/div[2]/span')
# seller = driver.find_elements(By.XPATH,'//div[contains(@class, "cWiizR")]')

# adr=[]
# pr=[]
# sl=[]
# for result in address:
#     adr.append(result.text)
# for result in price:
#     pr.append(result.text)
# for results in seller:
#     sl.append(result.text)


# with open("zillow.csv", "w") as f:
#     f.write("Address; Price; Seller\n")
# for i in range(len(adr)):
#     with open("zillow.csv", "a") as f:
#         f.write(str(adr[i])+"; "+str(pr[i])+"; "+str(sl[i])+"; "+str(sqr[i])+"\n")
# driver.quit()
