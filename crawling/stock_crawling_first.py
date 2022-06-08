import json
import pytz
import requests
import pandas as pd
from io import BytesIO
from datetime import timedelta
from datetime import datetime

data_path = './fullcode.csv'
save_path = './raw_data/'

def yesterday():
    tz = pytz.timezone('Asia/Seoul')
    raw_date = datetime.now(tz)
    yesterday = (raw_date - timedelta(1)).strftime("%Y%m%d")
    return yesterday


def crawling(fullcode):

  data2 = { 'bld': 'dbms/MDC/STAT/issue/MDCSTAT23902',
  'isuCd': fullcode,
  'isuCd2': '',
  'strtDd': strtDd,
  'endDd': endDd,
  'share': '1',
  'money': '1',
  'csvxls_isNo': 'false',}

  r2 = requests.post(url2, data2, headers)
  j2 = json.loads(r2.text)
  df2 = pd.DataFrame(j2['output'])

  data3 = { 'bld': 'dbms/MDC/STAT/standard/MDCSTAT03502',
  'isuCd': fullcode,
  'isuCd2': fullcode,
  'strtDd': strtDd,
  'endDd': endDd,
  'searchType': '2',
  'mktId': 'ALL',
  'csvxls_isNo': 'false',}

  r3 = requests.post(url2, data3, headers)
  j3 = json.loads(r3.text)
  df3 = pd.DataFrame(j3['output'])

  if len(df2.columns) > 0: #df2에 column이 존재하면 (df가 비어서 에러나는 경우 방지)
      df2_ = df2[['TRD_DD', 'ISU_CD', 'ISU_NM', 'TDD_CLSPRC', 'TDD_OPNPRC', 'TDD_HGPRC', 'TDD_LWPRC', 'MKTCAP', 'ACC_TRDVOL']]
  else: # df가 비었을때 column 생성.
      df2_ = pd.DataFrame(index = range(0,len(df3)),
                          columns = ['TRD_DD', 'ISU_CD', 'ISU_NM', 'TDD_CLSPRC', 'TDD_OPNPRC', 'TDD_HGPRC', 'TDD_LWPRC', 'MKTCAP', 'ACC_TRDVOL'])

  if len(df3.columns) > 0:
      df3_ = df3[['EPS', 'PER', 'BPS', 'PBR', 'DPS', 'DVD_YLD']]
  else:
      df3_ = pd.DataFrame(index = range(0,len(df2)),
                          columns = ['EPS', 'PER', 'BPS', 'PBR', 'DPS', 'DVD_YLD'])

  result = pd.concat([df2_, df3_], axis = 1)
  #print(result)

  # 데이터 저장
  result.to_csv(".".join([save_path + fullcode,"csv"]),index = False)


url2 = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',}

strtDd = '19000101'
endDd = yesterday()

fullcode = pd.read_csv(data_path)

# 상장폐지 상태 제외시키기
fullcode_filter = fullcode[fullcode['status'] != '상장폐지']

# fullcode열을 list로 변경
fullcode_list = list(fullcode_filter['full_code'])

for fullcode in fullcode_list:
  crawling(fullcode)
