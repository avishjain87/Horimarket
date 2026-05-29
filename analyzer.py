import yfinance as yf
import ta

def get_data(symbol, tf):
    return yf.download(symbol, period="5d", interval=tf)

def indicators(df):
    df["EMA9"] = ta.trend.ema_indicator(df["Close"], window=9)
    df["EMA21"] = ta.trend.ema_indicator(df["Close"], window=21)
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    return df

def confidence(last):
    score = 0

    if last["EMA9"] > last["EMA21"]:
        score += 35
    else:
        score += 10

    if last["RSI"] > 55:
        score += 25
    elif last["RSI"] < 45:
        score += 25
    else:
        score += 10

    return min(score, 100)

def signal(score, last):
    trend = "UP" if last["EMA9"] > last["EMA21"] else "DOWN"

    if score >= 80:
        return "🔥 HIGH ACCURACY BUY 🟨" if trend == "UP" else "🔥 HIGH ACCURACY SELL 🩷"
    elif score >= 70:
        return "BUY 🟨" if trend == "UP" else "SELL 🩷"
    elif score >= 55:
        return "⚠️ CAUTION"
    else:
        return "🚫 NO TRADE"

def analyze_market(name, symbol):
    df5 = indicators(get_data(symbol, "5m"))
    df15 = indicators(get_data(symbol, "15m"))

    last5 = df5.iloc[-1]
    last15 = df15.iloc[-1]

    score = int((confidence(last5) + confidence(last15)) / 2)

    sig = signal(score, last15)

    return f"""
📊 {name}
Score: {score}%
Signal: {sig}
"""
