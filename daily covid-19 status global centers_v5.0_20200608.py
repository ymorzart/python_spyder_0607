# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:04:06 2020

@author: vincent.yu
"""
import os

#해외센터 지역 코로나 현황 
# v1.0 top = 10 contries  
# v2.0 해외센터 대상지역 
# v3.0 대상 지역만 출력 
# v4.0 대상 지역만 출력
# v5.0 추가정리 보완 , 화일명 날짜포함 자동 변경 
#데이터 출처 : 위키백과European Centre for Disease Prevention and Control

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
#print(type(items))
#items = soup.find_all('tbody', class_='ppcUXd' )

#items = soup.find_all('tr', class_ = 'sgXwHf wdLSAe YvL7re', jsaction_=' click:KoQL8' )
#for itemss in items:
#    print(itemss.get_text())
#print(select_countries)
#print(len(items))

target_countries=["미국", "브라질", "러시아", "영국", "인도", "독일", "중국 대륙", "싱가포르", "베트남"]
# # 문자열 비교 
# match_list = [];
# target = "미국"
# for count in target_countries:
#     if target in count:
#         match_list.append(target)
# match_list
# print(match_list)

countries=[]; confirmeds=[]; confirmed_mills=[]; recovereds=[]; deaths=[];               
#limit = 100 #top = 10
#index = 0
#i = 0
#for item in items[:limit]: # top=10
for item in items: 
    #country = item.find('tr', {'class' :'sgXwHf wdLSAe YvL7re'}).text #에러!
    #country = item.find('div', {'class':'TWa0lb'}).text #국가, 전세계 포함
    country = item.find('div', {'class':'pcAJd'}).text #국가, 전세계 포함     
    countries.append(country)  
  
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
#print(df)
#대상 국가 filtering 
df2 = df[df["국가"].isin(target_countries)]
# df2.to_excel("K:/My files/Download/google_covid19_reporting_06081620.xlsx",index=False)
#cwd=os.getcwd()
#output_filepath=os.path.join(cwd,"output","google_trend_by_region_%s.png" % keyword)
datestring = datetime.strftime(datetime.now(),'%Y_%m_%d_%H_%M_%S')
df2.to_excel(excel_writer=r"K:/My files/Download/{0}".format('해외센터코로나현황_' + datestring + '.xlsx'))
print(df2)
