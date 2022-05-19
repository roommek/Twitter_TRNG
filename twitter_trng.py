import requests
import os
import json
import array
import matplotlib.pyplot as plt
import numpy as np
import time
import scipy.stats 
import pandas as pd

bearer_token = "AAAAAAAAAAAAAAAAAAAAAE7%2BcAEAAAAAdXgZ5nNCKF8bueTOCyTLQc9Hpn4%3Djkdyjav10STjlvDMNsIz8CprhmWC9mCVUGTOsHdHVRxAYeRQis"
#bearer_token = "AAAAAAAAAAAAAAAAAAAAAHEOcwEAAAAAlESlCOM88gnQ8kalyV3ff%2BzisJE%3D4uEZJMHVNB3TfmfEsYT8MLKfDIvhECuVVH7LVcQN4WrI8x2hFI"

search_url = "https://api.twitter.com/2/tweets/search/recent"

query_params = {'query': "\i",'max_results': '100', 'tweet.fields': 'text'}

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def colectTweets(t):
    json_response = connect_to_endpoint(search_url, query_params)
    for i in range(0, len(json_response['data'])):
        if(len(json_response['data'][i]['text']) <= 280): t.append(len(json_response['data'][i]['text']))

def main():
    t = []

    #for i in range(0, 3):
    for i in range(0, 449):
        colectTweets(t)
        print(i)
        #time.sleep(720)
    
    pd_series = pd.Series(t)
    counts = pd_series.value_counts()
    entr = scipy.stats.entropy(counts)
    print(entr)

    s = []
    int8 = []

    tOdd = t[1::2]
    tEven = t[::2] #parzyste

    temp = 0

    for i in range(0, int(len(t)/2)):
        temp = tOdd[i] - tEven[i]
        if(temp < 0): s.append(1)
        elif(temp == 0): continue
        else: s.append(0)

    b = len(s)%8
    for i in range(0, len(s)-b-8):
        int8.append(s[i] + s[i+1] * 2 + s[i+2] * 4 + s[i+3] * 8 + s[i+4] * 16 + s[i+5] * 32 + s[i+6] * 64 + s[i+7] * 128)
        
    for i in range(0, len(t)):
        t[i] = round(t[i]*0.91)

    pd_series2 = pd.Series(int8)
    counts2 = pd_series2.value_counts()
    entr2 = scipy.stats.entropy(counts2)
    print(entr2)

    fig, axs = plt.subplots(1, 2, figsize=[16, 8])
    axs[0].hist(t, 255, density=True)
    axs[0].set_title('Rozklad dlugosci wiadomosci T')
    axs[0].set_ylabel('Liczba probek')
    axs[0].set_xlabel('Dlugosc wiadomosci T[i]')

    axs[1].hist(int8, 255, density=True)
    axs[1].set_title('Rozklad liczb 8-bitowych po post procesingu')
    axs[1].set_ylabel('Liczba probek')
    axs[1].set_xlabel('Wartosc liczby 8-bitowej po post procesingu') 
    

    plt.show()

main()