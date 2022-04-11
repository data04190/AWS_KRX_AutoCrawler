import pickle
import json
import requests
import pandas as pd
from io import BytesIO
import pytz
from datetime import datetime, date, timedelta


headers = {'User-Agent': 'Chrome/93.0.4577.82 Safari/537.36,'}

data = {'mktsel': 'ALL',
         'typeNo': '0',
         'searchText': '',
         'bld': 'dbms/comm/finder/finder_stkisu',}

url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

r = requests.post(url,data,headers=headers)
j = json.loads(r.text)

df = pd.json_normalize(j['block1'])
df = df[['full_code','short_code','codeName','marketEngName']]

df['status'] = '상장'


df.to_csv('./fullcode.csv', index = False)
