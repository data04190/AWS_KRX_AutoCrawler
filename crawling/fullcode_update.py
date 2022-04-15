import pickle
import json
import requests
import pandas as pd
from io import BytesIO
import pytz
from datetime import datetime, date, timedelta


#일주일 날짜 구하기.
def today_date():   
  tz = pytz.timezone('Asia/Seoul')  #한국시간 맞추기.
  raw_dates = datetime.now(tz)
  day7_raw = raw_dates - timedelta(7) 
  day7 =  day7_raw.strftime("%Y%m%d")  # 일주일전 문자열로 변환
  today = raw_dates.strftime("%Y%m%d")  # 오늘 날짜 문자열로 변환
  return day7, today


#  상장 폐지 종목 불러오기 (KRX_상장폐지종목현황_화면번호(20037))
def week_delisting (day7,today):     

  headers = {'User-Agent': 'Chrome/93.0.4577.82 Safari/537.36,'}  

  url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

  data = {'bld': 'dbms/MDC/STAT/issue/MDCSTAT23801',
        'mktId': 'ALL',
        'tboxisuCd_finder_listdelisu0_0':'전체',
        'isuCd': 'ALL',
        'isuCd2': 'ALL',
        'codeNmisuCd_finder_listdelisu0_1':'',
        'param1isuCd_finder_listdelisu0_1':'',
        'strtDd': day7,
        'endDd': today, 
        'share': '1', 
        'csvxls_isNo': 'true',}

  r = requests.post(url,data,headers=headers)
  j = json.loads(r.text)

  df = pd.json_normalize(j['output'])

  if (len(df)==0): # 상장폐지 결과가 아예 없는 경우 
    return pd.DataFrame()  
  return df[['ISU_CD','ISU_NM','MKT_NM','DELIST_DD','DELIST_RSN_DSC']]  #종목코드, 종목명, 시장구분,증권구분, 폐지일, 폐지사유 열만 추출


# 신규상장기업현황 ( https://kind.krx.co.kr/listinvstg/listingcompany.do?method=searchListingTypeMain) 가져오기.
def new_listing(today): 

  headers = {'User-Agent': 'Chrome/93.0.4577.82 Safari/537.36,'} 

  data = {'method': 'searchListingTypeSub',
        'currentPageSize': '15',
        'pageIndex': '1',
        'orderMode': '1',
        'orderStat': 'D',
        'repIsuSrtCd': '',
        'isurCd': '',
        'forward': 'listingtype_sub',
        'listTypeArrStr': '01|02|03|04|05|',
        'choicTypeArrStr':'' ,
        'searchCodeType': '',
        'searchCorpName': '',
        'secuGrpArrStr': '0|ST|FS|MF|SC|RT|DR|',
        'marketType': '',
        'searchCorpNameTmp':'' ,
        'country': '410',
        'industry': '',
        'repMajAgntDesignAdvserComp': '',
        'repMajAgntComp': '',
        'designAdvserComp': '',
        'secuGrpArr': '0',
        'secuGrpArr': 'ST|FS',
        'secuGrpArr': 'MF|SC|RT',
        'secuGrpArr': 'DR',
        'listTypeArr': '01',
        'listTypeArr': '02',
        'listTypeArr': '03',
        'listTypeArr': '04',
        'listTypeArr': '05',
        'fromDate': today,
        'toDate': today,}

  url = "https://kind.krx.co.kr/listinvstg/listingcompany.do"

  r = requests.post(url,data,headers=headers)
  f = BytesIO(r.content)
  dfs = pd.read_html(f, encoding='UTF8' )
  df = dfs[0].copy()
  df = df.iloc[:,[0,1,2]]

  df =df.rename(columns = {'Unnamed: 0':'회사명','Unnamed: 1':'상장일','Unnamed: 2':'상장유형'})
  return df


# 신규상장  full_code krx에서 가져오기.
def KRX_search_fullcode(new_code):  
  headers = {'User-Agent': 'Chrome/93.0.4577.82 Safari/537.36,'}  

  data = {'mktsel': 'ALL',
        'typeNo': '0',
        'searchText': new_code,
        'bld': 'dbms/comm/finder/finder_stkisu',}

  url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

  r = requests.post(url,data,headers=headers)
  j = json.loads(r.text)

  df = pd.json_normalize(j['block1'])
  return df[['full_code','short_code','codeName','marketEngName']]


# 당일 상장폐지항목 df에서 상장폐지 상태로 변경하기.
def change_delisting(df, week_delisting,today): 

  for i in range (week_delisting.shape[0]) : 
    check = week_delisting.iloc[i,3] == today

    if (check):   #상장폐지 항목들이 오늘일 때만.
      len_shortcode = len(week_delisting.iloc[i,0])

      if (len_shortcode == 6) :  #종목코드 숫자가 6개일때만 (수익증권 같은 상장폐지항목은 저장된 df에 없기 때문에)
        index = df[df.codeName == week_delisting.iloc[i,1]].index
        df.iloc[index,4] = '상장폐지' 
        print(today)
        print(df.iloc[index,1]+' '+ df.iloc[index,2]+ '  상장폐지로 상태 변경')

  return df


#새로 상장된 주식 full_code에 추가하기
def change_new_listing (df,new_listing):

  result =  new_listing.iloc[0,0] != '조회된 결과값이 없습니다.'   

  if (result):  #신규 상장이 있으면.

    for i in range(new_listing.shape[0]):

      if (new_listing.iloc[i,2] == '신규상장') :
        new = KRX_search_fullcode(new_listing.iloc[i,0])
        new = new[new.codeName == new_listing.iloc[i,0]]   #이름 유사 종목 추가 방지.
        new['status']="상장"
        df = df.append(new, ignore_index = True)
        print(new.iloc[0,1]+' '+ new.iloc[0,2]+ ' 종목 추가')
        
      elif (new_listing.iloc[i,2] == '이전상장'):

        move_market = KRX_search_fullcode(new_listing.iloc[i,0])
        move_market = move_market[move_market.codeName == new_listing.iloc[i,0]]
        index = df[df['codeName']== new_listing.iloc[i,0]].index
        move_before = full_code.iloc[index,3]
        full_code.iloc[index,3]= move_market.iloc[i,3]
        print(new_listing.iloc[i,0]+' '+move_before+'에서 '+  move_market.iloc[i,3]+ '로 이전.')
        print('\n')

      elif (new_listing.iloc[i,2] == '재상장'):

        fullcode_search = full_code[full_code.codeName == new_listing.iloc[i,0]]

        if(len(fullcode_search) == 0): #상장폐지 항목에 없으면 full_code 밑에 새로 종목 추가.
          new = KRX_search_fullcode(new_listing.iloc[i,0])
          new = new[new.codeName == new_listing.iloc[i,0]]
          new['status']="상장"
          df = df.append(new, ignore_index = True)
          print(new.iloc[0,1]+' '+ new.iloc[0,2]+ ' 재상장')

  return df


# 최종 full_code 업데이트 함수.
def update_fullcode(df):

  day7, today = today_date()  #일주일 기간 날짜 구하기.
  print('일주일 전 : '+ day7)
  print('오늘 : '+ today+'\n') 


  print('-----------------------------------------------------------------------')
  print('한 주 상장폐지 종목 조회\n')
  week_delisting01 = week_delisting(day7,today) #한 주동안 상장폐지된 항목 조회
  if (len(week_delisting01)== 0):
    print("    한 주동안 상장폐지 결과 없음.")
    print('\n-------------------------------------------------------------------------\n')
  else:
    week_delisting01['DELIST_DD'] = week_delisting01['DELIST_DD'].str.replace('/','')
    print(week_delisting01+ '\n') 
    print(week_delisting01['DELIST_DD'])  
    print('\n-------------------------------------------------------------------------\n')

    df = change_delisting(df, week_delisting01, today) # 상장폐지 항목 df에서 상장폐지 상태 변경. 
    print('\n상장폐지 항목 상태 변경완료\n')
    print('-------------------------------------------------------------------------\n')

  # 신규상장 종목 조회
  print("당일 신규상장 종목 조회\n")
  new_listing01 = new_listing(today)
  print(new_listing01)
  print('\n-------------------------------------------------------------------------\n')

  #신규상장 상태 변경
  df = change_new_listing (df,new_listing01)
  print("신규상장 상태 변경 완료")
  print('\n-------------------------------------------------------------------------\n')

  return df


full_code = pd.read_csv('./fullcode.csv')
full_code = update_fullcode(full_code)
full_code.to_csv('./fullcode.csv', index = False)
