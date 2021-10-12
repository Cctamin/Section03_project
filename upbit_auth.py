import pyupbit
from upbit_key import access_key, secret_key

access_key = access_key
secret_key = secret_key
server_url = "https://api.upbit.com/v1/"


upbit = pyupbit.Upbit(access_key, secret_key)


# -* 현재 업비트의 상장된 원화 마켓 티커 추출
# ticker shape (ex> "KRW-BTC")
raw_tickers = pyupbit.get_tickers(fiat="KRW")
tickers = []
for i in raw_tickers:
    i = str(i).split('-')[1]
    tickers.append(i)



# ask = 매도, bid = 매수