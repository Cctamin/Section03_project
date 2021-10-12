import os
import sqlite3

from upbit_auth import upbit, tickers, raw_tickers

# Database 연결
DB_FILEPATH = os.path.join(os.getcwd(), "Database/trade_history.db")
conn = sqlite3.connect(DB_FILEPATH)
cur = conn.cursor()

# upbit_auth에서 만든 ticker list 불러오기
tickers = tickers
raw_tickers = raw_tickers

# ticker별 table 생성
# id, (주문)생성 날짜, (주문)생성 시간, 시장, 주문 형태, 가격, 매수/매도, volumne, 거래 총 가격)
for ticker in raw_tickers:
    ticker_name = str(ticker).split('-')[1]
    cur.execute(f"DROP TABLE IF EXISTS {ticker_name} ;")
    cur.execute(f"""CREATE TABLE {ticker_name} (
        id INTEGER PRIMARY KEY
        , created_date TEXT
        , created_time TEXT
        , market TEXT
        , ord_type TEXT
        , price REAL
        , side TEXT
        , volume REAL
        , trade_value REAL
            );""")

    # 티커별 주문 목록 불러오기
    order = upbit.get_order(ticker_or_uuid=ticker, state='done')
    i = 1
    order_many = []

    # 1개의 오더 씩 불러오기
    for order_num in order:
        created_at = str(order_num['created_at']).split('T')
        created_at_date = created_at[0]
        created_at_time = created_at[1].split('+')[0]
        market = order_num['market']
        ord_type = order_num['ord_type']
        price = order_num['price']
        side = order_num['side']
        volume = order_num['volume']
        if (volume == None) or (price == None):
            trade_value = None
        else:    
            trade_value = int(float(volume) * float(price))

        # db에 넣기 위해 튜플 형태로 data 저장
        order_tuple = (i, created_at_date, created_at_time,  market, 
                        ord_type,  price, side, volume, trade_value)
        
        order_many.append(order_tuple)
        i += 1
    
    # DB에 data 넣기
    cur.executemany(f"INSERT INTO {ticker_name} VALUES (?,?,?,?,?,?,?,?,?)", order_many)

conn.commit()
cur.close()