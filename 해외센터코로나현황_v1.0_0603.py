# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:28:50 2020

@author: vincent.yu
"""
#해외센터 지역 코로나 현황 Top=5
#대상: 미국, 브라질, 러시아, 영국, 인도, 독일, 중국, 싱가폴, 베트남,한국
#데이터 출처 : 위키백과European Centre for Disease Prevention and Control

import os

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


#from selenium import webdriver

#Today 
NOW = datetime.now() 
tYear = str(NOW.year) 
tMonth = str(NOW.month) 
if len(tMonth) == 1: 
    tMonth = '0'+tMonth 
 
 
tDay= str(NOW.day) 
if len(tDay) == 1: 
     tDay = '0'+tDay 
 
 
today = tYear+'-'+tMonth+'-'+tDay+' '+'한국시간.'
print(today)
print("\n")


#google base url 
base_url = "https://news.google.com/covid19/map?hl=ko&gl=KR&ceid=KR:ko"


resp = requests.get(base_url, verify = False)
html_src = resp.text
soup = BeautifulSoup(html_src,'html.parser')

#COVID-19 극가별 아이템 블럭을 선택
items = soup.select('tr[class="sgXwHf wdLSAe YvL7re"]') #전체 테이블 + 갯수 중요!!!
#print(items)
#print(len(items))

#countries=["미국", "브라질", "러시아", "영국", "인도", "독일", "중국", "싱가폴", "베트남","한국"]; contents=[] #;recovereds=[];deaths=[];

countries=[]; confirmeds=[];                  
limit = 5 #top = 5
for item in items[:limit]:
    # confirmed2 = item.find('tr', {'class': 'sgXwHf wdLSAe ROuVee'}).text #숫자 전부 
    # country = item.find('tr', {'class' :'sgXwHf wdLSAe YvL7re'}).text
    #country = item.find('div', {'class':'TWa0lb'}).text #국가, 전세계 포함
    country = item.find('div', {'class':'pcAJd'}).text #국가, 전세계 포함 
    #print(len(country))  
    #print(country)
    countries.append(country)
    #print(countries)

    confirmed = item.find('td', {'class': 'l3HOY'}).text #숫자 1개  
    #print(confirmed)
    confirmeds.append(confirmed)
    #print(countries, confirmeds)
        
    #content = country.replace('<td class="pcAJd">', ' ')
    #content = content.replace('</td>', ' ')
    #print(content)
    #contents.append(content)
    
result = {'country':countries,'confirmed':confirmeds}
df = pd.DataFrame(result, columns=['country','confirmed'])
    # df.to_excel("K:/My files/Download/google_covid19_reporting.xlsx")
print(df)
