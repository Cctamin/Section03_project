import os
import sqlite3
from upbit_auth import tickers

DB_FILEPATH = os.path.join(os.getcwd(), "Database/pre_USD_ETH.db")
conn = sqlite3.connect(DB_FILEPATH)
cur = conn.cursor()

tickers=["ETH"]

com_te=""
for ticker in tickers:
    for row in cur.execute(f"SELECT * FROM {ticker}"):
        for m in range(1,9):
            com_te = com_te + str(row[m]) +','
        com_te = com_te + "\n"

f = open("USD_ETH_history.csv","w")
f.write(com_te) 
f.close

cur.close()

print("done")