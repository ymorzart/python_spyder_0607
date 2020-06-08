# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:08:01 2020

@author: vincent.yu
"""
import os

#038.py

from pytrends.request import TrendReq
import matplotlib.pyplot as plt

keyword = "WTO"
period = "now-7d"

trend_obj = TrendReq()
trend_obj.build_payload(kw_list=[keyword],timeframe=period)

trend_df = trend_obj.interest_by_region().sort_values(ascending=False)
print(trend_df.head())

plt.style.use("ggplot")
plt.figure(figsize=(14,10))
trend_df.loc[:50,:][keyword].plot(kind='bar')
plt.titl("Google Trends by Region",size=15)
plt.legend(labels=[keyword],loc="upper right")

cwd=os.getcwd()
output_filepath=os.path.join(cwd,"output","google_trend_by_region_%s.png" % keyword)
plt.savefig(output_filepath, dpi=300)
plt.show()
