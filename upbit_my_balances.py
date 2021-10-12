import pyupbit
from upbit_auth import upbit

# 나의 보유 자산 불러오기
my_balance = upbit.get_balances()


# 보유중인 ticker만 불러오기
invest_tickers = []

for i in my_balance:
    ticker = i['currency']
    invest_tickers.append(ticker)

# 원화 및 비상장 ticker 제거 (원화는 따로 추가)
invest_tickers.remove('KRW')
invest_tickers.remove('APENFT')


# 보유 중인 자산의 balance 불러오기
balance = []
for ticker in invest_tickers:
    for j in my_balance:
        if j['currency'] == ticker:
            coin_value = float(j['balance'])
            balance.append(coin_value)
        else:
            pass

# 현재 금액 조회를 위해 ticker foramting (ex> 'KRW-BTC')
A = []
for i in invest_tickers:
    i = 'KRW-' + i
    A.append(i)


# 보유 중인 자산의 현재 금액 불러오기
current_price = []
for k in A:
    C = pyupbit.get_current_price(ticker=k)
    current_price.append(C)

# 보유중인 자산의 balance와 현재 price를 곱하여 보유중 자산 계산
my_total_balance = []
for x, y in zip(current_price, balance):
    real_balance = x * y
    my_total_balance.append(real_balance)

# 가지고 있는 원화 더하기
my_total_balance = int(sum(my_total_balance) + float(my_balance[0]['balance']))

# 현재 보유중인 자산 (금액 변동에 맞추어)
#live_my_balances = { "현재 보유 자산" : my_total_balance}


# 평균 매수 가격 (평단가)
order_balance = []
for i in my_balance:
    coin_value = float(i['balance']) * float(i['avg_buy_price'])
    order_balance.append(coin_value)

total_order_balance = int(sum(order_balance))
live_krw = round(float(my_balance[0]['balance']),2)

# 평단가 표시 및 매수 가능한 원화 표시
#invest_live = {"현재 매수 금액" : total_order_balance, "매수 가능한 금액" : live_krw}

# 수익률 표시
yeild = round((my_total_balance - total_order_balance)/total_order_balance*100,2)

