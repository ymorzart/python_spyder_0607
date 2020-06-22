# -*- coding: utf-8 -*-
"""
Created on Mon Jun  11 09:11:20 2020

@author: vincent.yu
"""
import os
os.environ["HTTP_PROXY"] = "http://70.10.15.10:8080"
os.environ["HTTPS_PROXY"] = "http://70.10.15.10:8080"
os.environ["PYTHONHTTPSVERIFY"] = "0"

#해외센터 지역 코로나 현황 
# v1.0 top = 10 contries  
# v2.0 해외센터 대상지역선정,v3.0범위조정 
# v4.0 대상 지역만 출력
# v5.0 추가정리 보완 , 화일명 날짜포함 자동 변경 
# v6.0 엑셀화일내 일시 제목 및 출처 표시
# v9.0 1차 Release 최종본 
#데이터 출처 : 위키백과European Centre for Disease Prevention and Control

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


#google base url 
base_url = "https://news.google.com/covid19/map?hl=ko&gl=KR&ceid=KR:ko"

resp = requests.get(base_url, verify = False)
html_src = resp.text
soup = BeautifulSoup(html_src,'html.parser')

#COVID-19 극가별 아이템 블럭을 선택
items = soup.select('tr[class="sgXwHf wdLSAe YvL7re"]') #전체 테이블 + 갯수 중요!!!
items2 = soup.select('tr[class="sgXwHf wdLSAe ROuVee"]') # 전세계 만

target_countries=["전세계", "미국", "브라질", "러시아", "영국", "인도", "독일", "중국 대륙", "싱가포르", "베트남"]

countries=[]; confirmeds=[]; confirmed_mills=[]; recovereds=[]; deaths=[];               

for ite in items2:
    #it = ite.find_all('td')
    globl = ite.find('div', {'class':'pcAJd'}).text
    
    numbers2 = ite.find_all('td')  #숫자 전부
    confirmed2 = numbers2[0].text.strip()

    confirmed_mill2 = numbers2[1].text       
    recovered2   = numbers2[2].text.strip()    
    death2 = numbers2[3].text.strip()

#result2 = {'국가': globl, '확진자수': confirmed2, '백만명당': confirmed_mill2, \
#           '완치자수' : recovered2, '사망자수': death2}
    
result2 = {'국가': globl, '확진자수': confirmed2, '완치자수' : recovered2, '사망자수': death2}    
#print (globl, confirmed2, death2)
# 전세계만 추출, Merge준비 
result3 = pd.DataFrame.from_dict(result2, orient='index').T
result3 = result3.reset_index()

for item in items: 
    country = item.find('div', {'class':'pcAJd'}).text  #국가 추출    
    countries.append(country)  
    
    numbers = item.find_all('td')  #숫자 전부
    confirmed = numbers[0].text.strip()                    # 확진자수 
    confirmeds.append(confirmed)             
    
    confirmed_mill = numbers[1].text                       #백만명당 확진자수
    confirmed_mills.append(confirmed_mill)
    
    recovered   = numbers[2].text.strip()                   #완치자수 
    recovereds.append(recovered)
    
    death = numbers[3].text.strip()                         #사망자수
    deaths.append(death)     
    
result = {'국가':countries,'확진자수':confirmeds,'백만명당':confirmed_mills, \
           '완치자수': recovereds,'사망자수': deaths}
df = pd.DataFrame(result, columns=['국가','확진자수','완치자수', '사망자수'])

#대상 국가 추출 
df2 = df[df["국가"].isin(target_countries)]
# 순위 정리 
df2 = df2.reset_index()
df2["index"] = df2["index"]+1
# 전세계와 대상국가 통합 
df2 = pd.concat([result3,df2], axis=0)
df2 = df2.rename(columns={"index":"순위"})
#df2.columns = pd.MultiIndex.from_product([['해외권역 COVID-19현황입니다.'],df2.columns])
datestring = datetime.strftime(datetime.now(),'%Y_%m_%d_%H_%M_%S')
df2.to_excel(excel_writer=r"K:/My files/Download/DC_COVID19/{0}".format('해외센터코로나현황_' + datestring + '.xlsx'),\
           index=False, #index_label ="순위",
           startrow=1, startcol=1,
             )
print(df2)
now = datetime.now()
print("{}-{}-{}[GMT+9]".format(now.year, now.month, now.day),"해외권역 COVID-19 현황")
print ("출처 : 위키백과European Centre for Disease Prevention and Control")
