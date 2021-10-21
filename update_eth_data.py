import os
import sqlite3
import time

import pyupbit
from upbit_auth import raw_tickers

# Database 연결
DB_FILEPATH = os.path.join(os.getcwd(), "Database/pre_USD_ETH.db")
conn = sqlite3.connect(DB_FILEPATH)
cur = conn.cursor()

raw_tickers = ["USDT-ETH"]

df = pyupbit.get_ohlcv(ticker=raw_tickers, count=30, interval="day") #, interval="day"

# db에 넣기 위해 데이터 튜플 형태로 저장
df.reset_index(inplace=True)

cur.execute("SELECT id FROM ETH e ORDER BY e.id DESC LIMIT 1")
id_number = cur.fetchone()
n = id_number[0] + 1

cur.execute("SELECT date FROM ETH e ORDER BY e.date DESC LIMIT 1")
pre_date = str(cur.fetchone()[0])

ohlcv_data = []
try:
    for i in list(range(len(df.index))):
        new_date = str(df.iloc[i]['index']).split(' ')[0]
        if pre_date != new_date:
            continue
        else :
            for j in list(range(i, len(df.index)+1)):
                row_data = df.iloc[j+1]
                ohlcv_data.append((n,
                                    str(row_data['index']).split(' ')[0],
                                    row_data['open'],
                                    row_data['high'],
                                    row_data['low'],
                                    row_data['close'],
                                    round(row_data['volume'],2),
                                    round((float(row_data['close'])-float(row_data['open']))/float(row_data['open'])*100,2),
                                    1 if float(row_data['close']) > float(row_data['open']) else 0
                                    ))
                n += 1
                
                time.sleep(0.3)
except:
    pass

cur.executemany(f"INSERT INTO ETH VALUES (?,?,?,?,?,?,?,?,?);", ohlcv_data)

conn.commit()
cur.close()