import datetime
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


def send_slack_alert(message, webhook_url):
    headers = {
        "Content-type": "application/json"
    }
    payload = {
        "text": message
    }
    response = requests.post(webhook_url, json=payload, headers=headers)
    response.raise_for_status()

def log_result(ticker, price, threshold, condition):
    timestamp = datetime.datetime.now().isoformat()
    with open("stock_log.csv", "a") as log_file:
        log_file.write(f"{timestamp},{ticker},{price},{threshold},{condition}")

if __name__ == "__main__":
    tickers = os.getenv("TICKERS").split(",")
    threshold = float(os.getenv("THRESHOLD"))
    webhook_url = os.getenv("SLACK_WEBHOOK")

    for ticker in tickers:
        ticker = ticker.strip().upper()
        price = get_stock_price(ticker)
        exceeded = price > threshold

        # Determine message and log entry
        if exceeded:
            message = f":chart_with_upwards_trend: *{ticker}* is at *${price:.2f}*, above the threshold of *${threshold:.2f}*."
            condition = "ABOVE"
        else:
            message = f":warning: *{ticker}* is at *${price:.2f}*, below or equal to the threshold of *${threshold:.2f}*."
            condition = "BELOW_OR_EQUAL"

        # Send Slack notification
        send_slack_alert(message, webhook_url)

        # Log result
        log_result(ticker, price, threshold, condition)

        # Print for Jenkins console logs
        print(f"[{condition}] {ticker} @ ${price:.2f} (Threshold: ${threshold:.2f})")
