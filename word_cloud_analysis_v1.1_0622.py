# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:03:06 2020

@author: vincent.yu

Word Cloud Analysis Eng Ver 1.0

"""
import os

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import requests
from bs4 import BeautifulSoup 
import time 
import requests
from datetime import datetime
import pandas as pd

# web page to file 
#import urllib
import urllib3.request
import html2text
#url=''
# page = urllib2.urlopen(url)
# html_content = page.read()
# rendered_content = html2text.html2text(html_content)
# file = open('file_text.txt', 'w')
# file.write(rendered_content)
# file.close()

#google base url, web page 분석, 영문만 가능해서 필터링 진행중....6/22
base_url = "https://en.wikipedia.org/wiki/COVID-19_pandemic"

page = urllib3.urlopen(base_url)
html_content = page.read()
rendered_content = html2text.html2text(html_content)


#resp = requests.get(base_url, verify = False)
#html_src = resp.text
#soup = BeautifulSoup(html_src, 'lxml')
#soup = BeautifulSoup(html_src,'html.parser')
#print(soup.get_text())

#text_m = soup.get_text()
##print(text_m)
text = open(rendered_content, encoding='utf-8').read()
print(text)


# 문서로 입력변수로 분석 
# 영어문서만 분석가능, 한글은 별도 

#현 작업 디렉토리
print("현재 폴더: ", os.getcwd())
# 디렉토리 변경 
os.chdir("K:\My files\Download\DC_COVID19_2")
print("변경 폴더: ", os.getcwd())

#작성된 영문자료 읽어서 분석 하는 자료 
#file_name = str(input("분석할 화일명을 입력하세요:"))
#text = open(file_name,encoding='utf-8').read()
#text = open("K:/My files/Download/DC_COVID19_2/John Bolton says_0621.txt",encoding='utf-8').read()


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
