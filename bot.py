import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your Telegram bot token from BotFather
TELEGRAM_API_TOKEN = 'YOUR_BOT_API_TOKEN'

# Function to get the TikTok video without watermark
def get_tiktok_video(link: str) -> str:
    api_url = f"https://tikcd.com/api/v1/tiktok?url={link}&no_watermark=true"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("download_url", "Failed to get the download URL.")
    return "Failed to download the video."

# Command to start bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a TikTok link, and I will fetch the video without a watermark.')

# Function to handle received messages
def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if "tiktok.com" in text:
        video_url = get_tiktok_video(text)
        update.message.reply_text(f"Here is your video: {video_url}")
    else:
        update.message.reply_text("Please send a valid TikTok link.")

# Main function to run the bot
def main() -> None:
    updater = Updater(TELEGRAM_API_TOKEN)
    dispatcher = updater.dispatcher
    
    # Adding command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Adding message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()