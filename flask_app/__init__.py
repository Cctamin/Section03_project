from flask import Flask, json, render_template, jsonify, request
from upbit_my_balances import my_total_balance, yeild, total_order_balance, live_krw, invest_tickers
import pyupbit
import pickle
import os
from pandas import DataFrame




app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/wallet')
def index():
    wallet = [my_total_balance,invest_tickers,total_order_balance,live_krw,yeild]
    return render_template('wallet.html', wallet=wallet)

@app.route('/')
def main():
    bitcoin = pyupbit.get_current_price(ticker="KRW-BTC")
    ethereum = pyupbit.get_current_price(ticker="KRW-ETH")
    ada = pyupbit.get_current_price(ticker="KRW-ADA")
    xrp = pyupbit.get_current_price(ticker="KRW-XRP")
    dot = pyupbit.get_current_price(ticker="KRW-DOT")

    coins=[bitcoin, ethereum, ada, xrp, dot]

    A = {"bit" : bitcoin, "eth" : ethereum}

    return render_template('main_list.html', coins=coins)

#filepath = os.path.join(os.getcwd(), "my_pickle.pkl")
#model = pickle.load(open('flask_app/model/price_predeict_model.pkl','rb'))
#model = load('flask_app/model/filename.joblib') 

@app.route('/pred', methods=['GET'])
def pred():
    """temp = request.args.get('open', "시작가")
    temp1 = request.args.get('high', "최고가")
    temp2 = request.args.get('low', "하한가")
    temp3 = request.args.get('volume', "볼륨")
    
    get_data = DataFrame([temp,temp1,temp2,temp3]).T
    
    prediction = model.predict(get_data)
    """
    answer = pickle.load(open('flask_app/model/simple_model.pkl', 'rb'))

    return answer

if __name__ == "__main__":
    app.run(debug=True)