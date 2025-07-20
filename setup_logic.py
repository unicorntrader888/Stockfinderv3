def is_green_candle(row):
    return row["Close"] > row["Open"]

def check_200ema_support(df):
    last = df.iloc[-1]
    return (
        is_green_candle(last)
        and abs(last["Close"] - last["200EMA"]) / last["Close"] < 0.01
        and last["Close"] > last["200EMA"]
    )

def check_30sma_support(df):
    last = df.iloc[-1]
    return (
        is_green_candle(last)
        and abs(last["Close"] - last["30SMA"]) / last["Close"] < 0.01
        and last["Close"] > last["30SMA"]
    )

def check_30sma_cip(df):
    last = df.iloc[-1]
    recent_closes = df["Close"].iloc[-6:-1]
    max_close = recent_closes.max()
    return (
        is_green_candle(last)
        and abs(last["Close"] - last["30SMA"]) / last["Close"] < 0.01
        and last["Close"] > last["30SMA"]
        and last["Close"] > max_close
    )

def check_ath_breakout(df):
    ath = df["Close"].max()
    last = df.iloc[-1]
    return is_green_candle(last) and last["Close"] >= ath

def check_30_200_combo(df):
    last = df.iloc[-1]
    near_30 = abs(last["Close"] - last["30SMA"]) / last["Close"] < 0.01
    near_200 = abs(last["Close"] - last["200EMA"]) / last["Close"] < 0.01
    return (
        is_green_candle(last)
        and last["Close"] > last["30SMA"]
        and last["Close"] > last["200EMA"]
        and (near_30 or near_200)
    )
