import os
import sqlite3
import time
import pandas as pd

# Database 연결
DB_FILEPATH = os.path.join(os.getcwd(), "Database/pre_USD_ETH.db")
conn = sqlite3.connect(DB_FILEPATH)
cur = conn.cursor()

ticker_name = "ETH"

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
    
    
# load the data into a Pandas DataFrame
eth = pd.read_csv('CSV_FILE/edit_ETH_USD.csv')

eth_param = []

try:
    n=1
    for i in list(range(len(eth.index))):
        row_data = eth.iloc[i]                
        eth_param.append((n,
                               row_data[0], # date
                               row_data[1], # open
                               row_data[2], # high
                               row_data[3], # low
                               row_data[4], # close
                               row_data[5], # volume
                               round((float(row_data[4])-float(row_data[1]))/float(row_data[1])*100,2),
                               1 if float(row_data[4]) > float(row_data[1]) else 0
                               ))
        n += 1
except:    
        print("Something wrong")

cur.executemany(f"INSERT INTO {ticker_name} VALUES (?,?,?,?,?,?,?,?,?);", eth_param)


conn.commit()
cur.close()