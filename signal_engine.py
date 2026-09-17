def generate_signal(df):
    if len(df) < 30:
        return {
            "signal": "WAIT",
            "confidence": 0,
            "reason": "Not enough market data"
        }

    latest = df.iloc[-1]

    score = 0
    reasons = []

    if latest["ema_fast"] > latest["ema_slow"]:
        score += 1
        reasons.append("EMA bullish")
    elif latest["ema_fast"] < latest["ema_slow"]:
        score -= 1
        reasons.append("EMA bearish")

    rsi = latest["rsi"]

    if rsi < 30:
        score += 1
        reasons.append("RSI oversold")
    elif rsi > 70:
        score -= 1
        reasons.append("RSI overbought")

    if latest["close"] > latest["sma_20"]:
        score += 1
        reasons.append("Price above SMA")
    else:
        score -= 1
        reasons.append("Price below SMA")

    if score >= 2:
        signal = "CALL"
    elif score <= -2:
        signal = "PUT"
    else:
        signal = "WAIT"

    confidence = min(abs(score) * 25, 75)

    return {
        "signal": signal,
        "confidence": confidence,
        "reason": ", ".join(reasons)
    }
