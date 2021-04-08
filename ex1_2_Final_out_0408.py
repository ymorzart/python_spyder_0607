#!/usr/bin/env python
# coding: utf-8

# -*- coding: utf-8 -*-

"""
[코드 3.33] 필요한 모듈들 임포트 (CH3. 데이터 수집하기 2.ipynb)
Source From Jupyter Project Ch3 데이터수집하기2.ipynb
가격데이터 추출 Jupter 버전 -> Spyder 버전 for Out
Modified on Thr April 8 09:30:00 2021
Created on Mon April 5 13:39:55 2021

@author: vincent.yu
"""
#[outer active 버전]
from datetime import datetime
import sdsutil
import requests
import bs4
import pandas as pd
import time
from utils_magic import *
datestring = datetime.strftime(datetime.now(),'%Y_%m_%d_%H_%M')
#현 작업 디렉토리
print("현재 폴더: ", os.getcwd())
# 디렉토리 변경 
os.chdir("K:\My files\Download\Python\Spyder\QT_part6\data")
print("변경 폴더: ", os.getcwd())
######

#  [코드 3.33] 필요한 모듈들 임포트 (CH3. 데이터 수집하기 2.ipynb)

#  [코드 3.34] 삼성전자 가격 데이터 요청하기 (CH3. 데이터 수집하기 2.ipynb)
price_url = 'https://fchart.stock.naver.com/sise.nhn?symbol=005930&timeframe=day&count=1500&requestType=0'
price_data = requests.get(price_url)



#  [코드 3.35] 뷰티풀스프화 하기 (CH3. 데이터 수집하기 2.ipynb)
price_data_bs = bs4.BeautifulSoup(price_data.text, 'lxml')

#  [코드 3.36] item 태그 찾아오기 (CH3. 데이터 수집하기 2.ipynb)
item_list = price_data_bs.find_all('item')

#  [코드 3.37] 첫 번째 데이터를 가져와서 잘라보기 (CH3. 데이터 수집하기 2.ipynb)

temp = item_list[0]['data']
temp.split('|')

#  [코드 3.38] 가져온 모든 태그에서 날짜와 종가만 출력하기 (CH3. 데이터 수집하기 2.ipynb)
for item in item_list:
    temp_data = item['data']
    datas = temp_data.split('|')
    print(datas[0], datas[4])

#  [코드 3.39] 가져온 모든 태그에서 날짜와 종가를 저장하여 데이터프레임으로 만들기 (CH3. 데이터 수집하기 2.ipynb)

date_list = []
price_list = []
for item in item_list:
    temp_data = item['data']
    datas = temp_data.split('|')
    date_list.append(datas[0])
    price_list.append(datas[4])
    
price_df = pd.DataFrame({'종가':price_list}, index=date_list)


#  [코드 3.40] 가격을 가져와 데이터프레임 만드는 함수 (CH3. 데이터 수집하기 2.ipynb)

def make_price_dataframe(code, timeframe, count):
    url = 'https://fchart.stock.naver.com/sise.nhn?requestType=0'
    price_url = url + '&symbol=' + code + '&timeframe=' + timeframe + '&count=' + count
    price_data = requests.get(price_url)
    price_data_bs = bs4.BeautifulSoup(price_data.text, 'lxml')
    item_list = price_data_bs.find_all('item')
    
    date_list = []
    price_list = []
    for item in item_list:
        temp_data = item['data']
        datas = temp_data.split('|')
        date_list.append(datas[0])
        price_list.append(datas[4])

    price_df = pd.DataFrame({code:price_list}, index=date_list)
    
    return price_df

#  [코드 3.41] 가격 데이터프레임 만드는 함수 사용 (CH3. 데이터 수집하기 2.ipynb)

make_price_dataframe('005380', 'day', '1500')

#  [코드 3.42] 여러 회사의 종가를 가져와 하나의 데이터프레임으로 만들기 (CH3. 데이터 수집하기 2.ipynb)

firmcode_list = ['005930', '005380', '035420', '003550', '034730']

for num, code in enumerate(firmcode_list):
    price_df = make_price_dataframe(code, 'day', '1500')
    if num == 0 :
        total_price = price_df
    else:
        total_price = pd.merge(total_price, price_df, how='outer', right_index=True, left_index=True)
        
# firmcode_list 종목을 total_price로 엑셀로 저장하기 가능

#  [코드 3.43] 전체 회사코드 가져오기 (CH3. 데이터 수집하기 2.ipynb)

path = r'K:\My files\Download\Python\Spyder\QT_part6\data\data.xls'
#code_data = sdsutil.read_excel(r"K:\My files\Download\Python\Spyder\QT_part6\data\data.xlsx")
code_data = sdsutil.read_excel(path)
#code_data = pd.read_excel(path)
code_data = code_data[['종목코드', '기업명']]

def make_code2(x):
    x = str(x)
    return '0' * (6-len(x)) + x

code_data['종목코드'] = code_data['종목코드'].apply(make_code2)


#  [코드 3.44] 가격 데이터 다 가져오기 (CH3. 데이터 수집하기 2.ipynb)
for num, code in enumerate(code_data['종목코드']):
    try:
        print(num, code)
        time.sleep(1)
        try:
            price_df = make_price_dataframe(code, 'day', '1500')
        except requests.exceptions.Timeout:
            time.sleep(60)
            price_df = make_price_dataframe(code, 'day', '1500')
        if num == 0 :
            total_price = price_df
        else:
            total_price = pd.merge(total_price, price_df, how='outer', right_index=True, left_index=True)
    except ValueError:
        continue
    except KeyError:
        continue

#  [코드 3.45] 인덱스 시간 데이터로 바꾸고 엑셀로 저장하기 (CH3. 데이터 수집하기 2.ipynb)
total_price.index = pd.to_datetime(total_price.index)
total_price.to_excel(r'K:\My files\Download\Python\Spyder\QT_part6\data\가격데이터.xlsx')
