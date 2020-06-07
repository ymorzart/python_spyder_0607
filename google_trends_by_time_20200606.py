# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:20:18 2020

@author: vincent sooy
© 2020 vincent.yu@samsung.com 
"""

#037.py 

from pytrends.request import TrendReq 
#No module named 'pytrends' 해결 : anaconda prompt -> pip install pytrens
import matplotlib.pyplot as plt
#import pandas as pd
import os

keyword = "Galaxy S20"
period = "today 3-m"

trend_obj = TrendReq()
trend_obj.build_payload(kw_list=[keyword], timeframe=period)

trend_df = trend_obj.interest_over_time()
print(trend_df.head())

plt.style.use("ggplot")
plt.figure(figsize=(14,5))
trend_df["Galaxy S20"].plot()
plt.title("Google Trends over Time",size=15)
plt.legend(labels=["Galaxy S20"],loc="upper right")

cwd=os.getcwd()
output_filepath=os.path.join(cwd,"output","google_trend_%s.png" % keyword)
plt.savefig(output_filepath, dpi=300)
plt.show()