import os
import re
import json
import pytz
import requests
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta

data_path = './fullcode.csv'
save_path = './raw_data/'

def yesterday():

    tz = pytz.timezone('Asia/Seoul')
    raw_date = datetime.now(tz)
    yesterday = (raw_date - timedelta(1)).strftime("%Y%m%d")
    return yesterday


def crawling(fullcode):

  global result

  data2 = { 'bld': 'dbms/MDC/STAT/issue/MDCSTAT23902',
  'isuCd': fullcode,
  'isuCd2': '',
  'strtDd': strtDd,
  'endDd': endDd,
  'share': '1',
  'money': '1',
  'csvxls_isNo': 'false',}

  r2 = requests.post(url2, data2, headers)
  print(r2)
  print(type(r2))
  if (r2 == "<Response [403]>"):
      print("에러발생")
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
  print(result)


url2 = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',}
#headers = {"User-Agent": "Mozilla/5.0"}


fullcode = pd.read_csv(data_path)

# 상장폐지 상태 제외시키기
fullcode_filter = fullcode[fullcode['status'] != '상장폐지']

# fullcode열을 list로 변경
fullcode_list = list(fullcode_filter['full_code'])

#파일 리스트 목록 가져오기
file_list = os.listdir(save_path)


for i in range(len(fullcode_list)):

  fullcode_file = ".".join([fullcode_list[i],'csv'])

  if fullcode_file in file_list:

    df = pd.read_csv(save_path+fullcode_file)

    try:

      latest_date = df.loc[0,'TRD_DD']
      latest_date = re.sub('/','-',latest_date)
      latest = datetime.strptime(latest_date, '%Y-%m-%d') + timedelta(days = 1)  #가장 최근 날짜 +1
      latest = latest.strftime("%Y%m%d")

      strtDd = latest # 가장 최근 수집된 다음날부터
      endDd = yesterday() #전날까지 수집.

      print(strtDd)
      print(endDd)
      if(strtDd > endDd):
          print(i+1," ", fullcode_list[i]," 업데이트 완료")
          continue


      crawling(fullcode_list[i])

      result1 = pd.concat([result, df], axis = 0, ignore_index = True)
      #print(result1)

      # 데이터 저장
      result1.to_csv(".".join([save_path + fullcode_list[i],"csv"]),index = False)
      print(i+1,"번째 ", fullcode_list[i])
      #print(result1)
    except:

      strtDd = 19000101
      endDd = yesterday()

      crawling(fullcode_list[i])

      result.to_csv(".".join([save_path + fullcode_list[i],"csv"]),index = False)
      print(i+1,"번째 ", fullcode_list[i], "except문 작동")


  elif fullcode_file not in file_list: # 신규상장

    strtDd = 19000101
    endDd = yesterday()

    crawling(fullcode_list[i])

    result.to_csv(".".join([save_path + fullcode_list[i],"csv"]),index = False)
    print(i+1,"번째 ", fullcode_list[i], "신규 상장")
