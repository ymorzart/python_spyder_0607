# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 23:28:24 2020

@author: vincent sooy
© 2020 vincent.yu@samsung.com 
"""

#해외센터 지역 코로나 현황 
# v1.0 top = 10 contries  
# v2.0 해외센터 대상지역 
# v3.0 대상 지역만 출력 
#대상: 미국, 브라질, 러시아, 영국, 인도, 독일, 중국, 싱가폴, 베트남,한국
#데이터 출처 : 위키백과European Centre for Disease Prevention and Control

#import os
#os.environ["HTTP_PROXY"] = "http://70.10.15.10:8080"
#os.environ["HTTPS_PROXY"] = "http://70.10.15.10:8080"
#os.environ["PYTHONHTTPSVERIFY"] = "0"

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
#from selenium import webdriver

now = datetime.now()
#print("now date and time : " + str(now))
# print("now year : " + str(now.year))
# print("now month : " + str(now.month))
# print("now day : " + str(now.day))
# print("now hour : " + str(now.hour))
# print("now min : " + str(now.minute))
# print("now second : " + str(now.second))
print("한국시간[GMT+9] : {}-{}-{}".format(now.year, now.month, now.day))

#Today 
# NOW = datetime.now()
# tYear = str(NOW.year) 
# tMonth = str(NOW.month) 
# tDay= str(NOW.day) 
# tTime = str(NOW.time)
# today = tYear+'-'+tMonth+'-'+tDay+' '+'한국시간.' 
# today = tYear+'-'+tMonth+'-'+tDay+''+'[GMT+9]'
# #print(today)
# print("\n")


#google base url 
base_url = "https://news.google.com/covid19/map?hl=ko&gl=KR&ceid=KR:ko"


resp = requests.get(base_url, verify = False)
html_src = resp.text
soup = BeautifulSoup(html_src,'html.parser')

#COVID-19 극가별 아이템 블럭을 선택
items = soup.select('tr[class="sgXwHf wdLSAe YvL7re"]') #전체 테이블 + 갯수 중요!!!
#items = soup.select('div[class="ppcUXd"]')
#items = soup.select('div[class="sOh CrmLxe"]')
#items = soup.select('#yDmH0d > c-wiz > div > div.FVeGwb.ARbOBb > div.BP0hze > div.y3767c > div > div > div.dzRe8d.pym81b > \
                      # div > div.sOh.CrmLxe > table > tbody')
#items = soup.select('tr[class="sgXwHf wdLSAe YvL7re"]')
#print(select_countries)
#print(len(items))

#target_countries=["미국", "브라질", "러시아", "영국", "인도", "독일", "중국", "싱가폴", "베트남"]
#match_list = [];
#for target in items:
#    if target_countries in target:
#        match_list.append(target)
#match_list
#print(match_list)

all_countries=[]; countries=[]; confirmeds=[]; confirmed_mills=[]; recovereds=[]; deaths=[];               
#limit = 10 #top = 10
#index = 0
#i = 0
for item in items: # top=10
#for item in items: 
    #country = item.find('tr', {'class' :'sgXwHf wdLSAe YvL7re'}).text #에러!
    #country = item.find('div', {'class':'TWa0lb'}).text #국가, 전세계 포함
    country = item.find('div', {'class':'pcAJd'}).text #국가, 전세계 포함     
    countries.append(country)  
    
    #print(countries) 
    #if countries == "미국":
    numbers = item.find_all('td')  #숫자 전부
    confirmed = numbers[0].text.strip()
    confirmeds.append(confirmed)
    
    confirmed_mill = numbers[1].text
    confirmed_mills.append(confirmed_mill)
    
    recovered   = numbers[2].text.strip()
    recovereds.append(recovered)
    
    death = numbers[3].text.strip()
    deaths.append(death)    
    
    #confirmed2 = confirmed2[0]
    #print(first,second,third, fourth)   
   
    
result = {'국가':countries,'확진자수':confirmeds,'백만명당':confirmed_mills, \
           '완치자수': recovereds,'사망자수': deaths}
df = pd.DataFrame(result, columns=['국가','확진자수','완치자수', '사망자수'])
#df.to_excel("K:/My files/Download/google_covid19_reporting_06051640.xlsx")
#df.to_excel("C:/Vincent/torrent/Download/PYTHON/Spyder Projects/Start of June/google_covid19_reporting_06051640.xlsx")
print(df)
    
#news_reporting_date = news_reporting_datetime[0]
#news_reporting_time = news_reporting_datetime[1][:-1]
#reporting_dates.append(news_reporting_date)
#reporting_times.append(news_reporting_time)
