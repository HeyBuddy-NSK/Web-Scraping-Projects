#!/usr/bin/env python
# coding: utf-8

# In[142]:

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



while True:
    url = "https://coinmarketcap.com/"

    hdrs = {'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
               'Accept-Language':'en-US,en;q=0.9'}


    url_response = requests.get(url, hdrs)


    print("response :: ",url_response.ok)


    # # Making soup
    url_soup = BeautifulSoup(url_response.content,"lxml")


    # # getting tables from website
    tables = url_soup.find_all("table")


    all_rows_with_tags = {}
    all_tr_tags = []

    for table in tables:
        tr_tags = table.find_all("tr")
        
        for i, tr in enumerate(tr_tags):
            all_td_tags = []
            td_tags = tr.find_all("td")
            all_tr_tags.append(tr)
            
            
            for td in td_tags:
                all_td_tags.append(td)
                
            if i>0:
                all_rows_with_tags[i]=all_td_tags


    # Getting data of top 10 crypto currencies.
    top_10_crypto_data = []

    for i in range(1,11):
        crypt_data = []

        for td in all_rows_with_tags[i]:
            td_data = td.text.strip()
            if td_data !="":
                crypt_data.append(td_data)

        top_10_crypto_data.append(crypt_data)



    # Creating dictionary for names and prices of top 10 cryptos
    crypto_names_prices = {}

    # getting names and prices
    top_10_crypto_names = []
    top_10_crypto_price = []

    for i in top_10_crypto_data:
    
        for j in range(1,3):
            if j==1:
                top_10_crypto_names.append(i[j])
            else:
                top_10_crypto_price.append(i[j])
            

    # Formatting ambiguited names
    formatted_top_10_crypto_names = []

    for i,name in enumerate(top_10_crypto_names,1):
        split_name = name.split(f"{i}")
        # print(split_name)
        formatted_top_10_crypto_names.append(split_name[0])


    # converting string price to numeric
    numeric_top_10_crypto_price = []

    for price in top_10_crypto_price:
        price1 = price.split("$")
        for t in price1:
            if t!="":
                t1 = t.split(",")
                numeric_top_10_crypto_price.append(float("".join(t1)))

    # storing in dict.
    crypto_names_prices['name'] = formatted_top_10_crypto_names
    crypto_names_prices["price"] = numeric_top_10_crypto_price


    # creating dataframe of data
    top10 = pd.DataFrame(crypto_names_prices,index=[1,2,3,4,5,6,7,8,9,10])

    print(top10)


    # Plotting bar chart of data
    top10.plot.bar(x='name',y='price')

    # waiting for next request.
    time.sleep(300)