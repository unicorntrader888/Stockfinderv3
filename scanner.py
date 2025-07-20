import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt
from setup_logic import (
    check_200ema_support,
    check_30sma_support,
    check_30sma_cip,
    check_ath_breakout,
    check_30_200_combo
)

nifty_500_symbols = pd.read_csv("nifty500.csv")["Symbol"].tolist()

def get_stock_data(symbol, timeframe):
    interval = {"2H": "2h", "Daily": "1d"}[timeframe]
    df = yf.download(symbol + ".NS", period="3mo", interval=interval)
    df["20EMA"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["30SMA"] = df["Close"].rolling(window=30).mean()
    df["200EMA"] = df["Close"].ewm(span=200, adjust=False).mean()
    return df

def save_chart(df, symbol):
    plt.figure(figsize=(10, 4))
    plt.plot(df["Close"], label="Close", color="black")
    plt.plot(df["30SMA"], label="30 SMA", linestyle="--")
    plt.plot(df["200EMA"], label="200 EMA", linestyle="--")
    plt.title(symbol)
    plt.legend()
    filename = f"charts/{symbol}.png"
    os.makedirs("charts", exist_ok=True)
    plt.savefig(filename)
    plt.close()
    return filename

def scan_stocks(setup, timeframe):
    matched = []
    check_fn = {
        "200 EMA Support": check_200ema_support,
        "30 SMA Support": check_30sma_support,
        "30 SMA CIP": check_30sma_cip,
        "ATH Breakout": check_ath_breakout,
        "30 + 200 Combo": check_30_200_combo
    }[setup]

    for symbol in nifty_500_symbols:
        try:
            df = get_stock_data(symbol, timeframe)
            if len(df) < 30:
                continue
            if check_fn(df):
                chart_path = save_chart(df, symbol)
                matched.append({"symbol": symbol, "chart": chart_path})
        except Exception as e:
            continue

    return matched
