import requests as rq
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

