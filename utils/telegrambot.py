import os
from telegram import Bot

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

def send_to_telegram(message):
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    bot.send_message(chat_id=chat_id, text=message)
