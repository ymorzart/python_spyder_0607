import os
os.environ["HTTP_PROXY"] = "http://70.10.15.10:8080"
os.environ["HTTPS_PROXY"] = "http://70.10.15.10:8080"
os.environ["PYTHONHTTPSVERIFY"] = "0"

import pandas as pd
import requests
import bs4

column_names = ["Country name", "Total cases", "New cases", "Total deaths",\
                "New deaths"] #"Total Recovered", "Active cases"]
df = pd.DataFrame(columns = column_names)

res = requests.get("https://www.worldometers.info/coronavirus", verify=False)
country= ["USA","Brazil","Russia","UK","India","Germany","China","Singapore","Vietnam","S. Korea"]
soup = bs4.BeautifulSoup(res.text, 'lxml')


for j in range(len(country)):
    index = -1
    data=soup.select('tr td')
    for i in range(len(data)):
        if data[i].text.lower()==country[j].lower():
            index=i
            break
    df.at[j,"Country name"]    = str(data[0+index].text)
    df.at[j,"Total cases"]     = str(data[1+index].text)
    df.at[j,"New cases"]       = str(data[2+index].text)
    df.at[j,"Total deaths"]    = str(data[3+index].text)
    df.at[j,"New deaths"]      = str(data[4+index].text)
   # df.at[j,"Total Recovered"] = str(data[5+index].text)
   # df.at[j,"Active cases"]    = str(data[7+index].text)

print(df)
