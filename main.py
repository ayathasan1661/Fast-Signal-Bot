from market_data import get_market_data
from indicators import add_indicators
from signal_engine import generate_signal
from telegram_bot import send_telegram
from config import MARKET_SYMBOL, TIMEFRAME
from logger import logger


def main():
    logger.info("Fast Signal Bot started.")

    try:
        df = get_market_data()
        df = add_indicators(df)

        result = generate_signal(df)

        latest_price = df.iloc[-1]["close"]

        message = (
            "🚦 FAST SIGNAL BOT\n\n"
            f"Market: {MARKET_SYMBOL}\n"
            f"Timeframe: {TIMEFRAME}\n"
            f"Price: {latest_price}\n\n"
            f"Signal: {result['signal']}\n"
            f"Confidence: {result['confidence']}%\n\n"
            f"Analysis: {result['reason']}\n\n"
            "⚠️ Educational market analysis — "
            "not a guaranteed trading result."
        )

        logger.info(message)

        send_telegram(message)

        logger.info("Telegram message sent.")

    except Exception as error:
        logger.exception("Bot error: %s", error)


if __name__ == "__main__":
    main()
