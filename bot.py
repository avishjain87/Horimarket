import datetime
import time
from telegram import Bot
from analyzer import analyze_market
from markets import MARKETS

TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

bot = Bot(token=TOKEN)

def send_report():
    msg = "📊 DAILY ADVANCED REPORT\n\n"

    for name, symbol in MARKETS.items():
        try:
            msg += analyze_market(name, symbol) + "\n\n"
        except:
            msg += f"{name}: ERROR\n\n"

    bot.send_message(chat_id=CHAT_ID, text=msg)

def run():
    while True:
        hour = datetime.datetime.now().hour

        if 8 <= hour <= 23:
            send_report()
            print("Sent")

        time.sleep(300)

if __name__ == "__main__":
    run()
