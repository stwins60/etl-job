import yfinance as yf
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    price = stock.history(period="1d")['Close'].iloc[-1]
    # high_price = stock.history(period="1d")['High'].iloc[-1]
    # low_price = stock.history(period="1d")['Low'].iloc[-1]
    return price


def send_slack_alert(ticker, price, threshold, webhook_url):
    headers = {
        "Content-type": "application/json"
    }
    if price > threshold:
        message = {
            "text": f""":chart_with_upwards_trend: *{ticker}* has reached ${price:.2f}, exceeding the treshold
            of ${threshold:.2f}!
            """
        }
    else:
        message = {
            "text": f""":chart_with_downwards_trend: *{ticker}* has reached ${price:.2f}, lower/equal to the treshold
            of ${threshold:.2f}!
            """
        }
    response = requests.post(webhook_url, json=message, headers=headers)
    response.raise_for_status()

if __name__ == "__main__":
    ticker = os.getenv("TICKER")
    threshold = float(os.getenv("THRESHOLD"))
    webhook_url = os.getenv("SLACK_WEBHOOK")

    price = get_stock_price(ticker)

    print(f"[INFO] Current price if {ticker}: ${price:.2f}")
    if price > threshold:
        print(f"[ALERT] {ticker} price ${price:.2f} > threshold of ${threshold:.2f}")
        send_slack_alert(ticker, price, threshold, webhook_url)
    else:
        print(f"[ALERT] {ticker} price ${price:.2f} <= threshold of ${threshold:.2f}")
        send_slack_alert(ticker, price, threshold, webhook_url)