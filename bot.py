import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram bot token (Replace with your bot token)
TOKEN = "6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU"

# API URL
API_URL = "https://subhatde.id.vn/tiktok/downloadvideo?url={}"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a TikTok video link, and I'll fetch the download link for you!")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text

    if "tiktok.com" not in user_text:
        update.message.reply_text("Please send a valid TikTok video link.")
        return

    # Call API
    response = requests.get(API_URL.format(user_text))
    
    if response.status_code == 200:
        update.message.reply_text(f"Download Link: {response.text}")
    else:
        update.message.reply_text("Failed to fetch video. Please try again.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()