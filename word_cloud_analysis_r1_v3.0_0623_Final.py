# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:03:06 2020

@author: vincent.yu

Word Cloud Analysis Eng Ver 3.0
Web Site to Text file and analysis Word Cloud 
"""
import os


from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
from bs4 import BeautifulSoup 
import time 
from datetime import datetime
import requests

# 영문 web page 선택 
#base_url = "https://en.wikipedia.org/wiki/Wikipedia:Contact_us"
base_url = "https://en.wikipedia.org/wiki/COVID-19_pandemic"

# Web Page 입력 
resp = requests.get(base_url,verify = False)
html_src = resp.text
soup = BeautifulSoup(html_src,'html.parser')
# 화일 생성 
with open('K:/My files/Download/DC_COVID19_2/file.txt', mode='w', encoding='utf-8')  as file:
     file.write(soup.text)

# 문서로 입력변수로 분석, 영어문서만 분석가능, 한글은 별도 
text = open('K:/My files/Download/DC_COVID19_2/file.txt', encoding='utf-8').read()

#현 작업 디렉토리
print("현재 폴더: ", os.getcwd())
# 디렉토리 변경 
os.chdir("K:\My files\Download\DC_COVID19_2")
print("변경 폴더: ", os.getcwd())

##별도 작성된 영문자료 읽어서 분석 할때 사용## 
#file_name = str(input("분석할 화일명을 입력하세요:"))
#text = open(file_name,encoding='utf-8').read()

#text 입력변수 분석
wordcloud = WordCloud(background_color='white',
                       width = 1920,
                       height = 1080).generate(text)
fig = plt.figure()
plt.imshow(wordcloud, interpolation='bilinear',cmap='YlOrBr')
plt.axis('off')

#화일명에 현재일자포함
datestring = datetime.strftime(datetime.now(),'%Y_%m_%d_%H_%M_%S')
plt.savefig('K:/My files/Download/DC_COVID19_2/Word_'+ datestring +'.png')
#plt.savefig('K:/My files/Download/DC_COVID19_2/Word_'+ file_name + datestring +'.png')
