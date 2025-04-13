import os
import asyncio
from dotenv import load_dotenv
from fetch.rss_fetcher import fetch_news
from process.summarizer import summarize_article
from telegram import Bot

# Load environment variables
load_dotenv()

# Get Telegram credentials from the environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_telegram_message(message):
    """Send a message via Telegram Bot"""
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    print("Message sent on Telegram")

def main():
    keywords = ["semiconductor", "chips", "technology"]  # Keywords to filter news
    articles = fetch_news(keywords)

    # Generate a summary for each article and send it via Telegram
    summary_message = "Good Morning! Here's your daily semiconductor news summary:\n\n"
    for article in articles[:5]:  # Top 5 articles
        summary = summarize_article(article['text'])
        summary_message += f"[{article['source']}] {article['title']}\nSummary: {summary}\n{article['link']}\n\n"

    # Send the summary as a Telegram message
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_telegram_message(summary_message))

if __name__ == "__main__":
    main()
