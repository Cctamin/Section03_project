import os
import sqlite3
import time

import pyupbit
from upbit_auth import raw_tickers

# Database 연결
DB_FILEPATH = os.path.join(os.getcwd(), "Database/coin_ohlcv.db")
conn = sqlite3.connect(DB_FILEPATH)
cur = conn.cursor()

# ticker별 ohlcv table 생성
# id, 날짜, 시초가, 최고가, 최저가, 마감가, volumne, 전일 대비 변동률, 올랐으면 1 안 올랐으면 0
for ticker in raw_tickers:
    ticker_name = str(ticker).split('-')[1]
    cur.execute(f"DROP TABLE IF EXISTS {ticker_name} ;")
    cur.execute(f"""CREATE TABLE {ticker_name} (
        id INTEGER PRIMARY KEY
        , date TEXT
        , open REAL
        , high REAL
        , low REAL
        , close REAL
        , volume REAL
        , rate_of_change REAL
        , up_or_down INTEGER   );""")
    
    # 최대 200개의 요청까지 가능
    df = pyupbit.get_ohlcv(ticker=ticker, count=180, interval="minute240") 

    # db에 넣기 위해 데이터 튜플 형태로 저장
    df.reset_index(inplace=True)
    ohlcv_data = []
    try:
        n = 1
        for i in list(range(len(df.index))):
            row_data = df.iloc[i]
            ohlcv_data.append((n,
                               str(row_data['index']).split(' ')[0],
                               row_data['open'],
                               row_data['high'],
                               row_data['low'],
                               row_data['close'],
                               round(row_data['volume'],2),
                               (float(row_data['open'])-float(row_data['close']))/float(row_data['open'])*100,
                               1 if float(row_data['close']) > float(row_data['open']) else 0
                               ))
            n += 1
    except:    
        print(ticker)

    # write data in db
    cur.executemany(f"INSERT INTO {ticker_name} VALUES (?,?,?,?,?,?,?,?,?);", ohlcv_data)
    
    # 업비트 자체에서 초당 5회 이하의 요청으로 제한해 두었기에 딜레이를 줌 -> 딜레이 안주면 요청 거절 당함
    time.sleep(0.3)


conn.commit()
cur.close()