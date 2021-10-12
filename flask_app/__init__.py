from flask import Flask, render_template
from upbit_my_balances import my_total_balance, yeild, total_order_balance, live_krw, invest_tickers

app = Flask(__name__)

@app.route('/wallet')
def index():
    wallet = { " live balance " : my_total_balance,
               " tickers " : invest_tickers,
               " ordered balance " : total_order_balance,
               " orderable krw " : live_krw,
               " yeild " : yeild
    }
    return wallet

@app.route('/chart')
def trade():
    return 

if __name__ == "__main__":
    app.run(debug=True)