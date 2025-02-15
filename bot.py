import logging
import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables from .env file (for local development)
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the API URL and function to get the TikTok video
def get_tiktok_video(video_url):
    api_url = f"https://api.sumiproject.net/tiktok?video={video_url}"
    response = requests.get(api_url)
    data = response.json()
    return data.get('download_url')

# Start Command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me a TikTok video link, and I will download it for you.')

# Function to handle video link
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if "tiktok.com" in text:  # Simple check if the message contains a TikTok link
        download_url = get_tiktok_video(text)
        if download_url:
            await update.message.reply_text(f"Your TikTok video download link: {download_url}")
        else:
            await update.message.reply_text("Sorry, I couldn't fetch the video. Please try again later.")
    else:
        await update.message.reply_text("Please send a valid TikTok video link.")

def main():
    # Get the Telegram Bot Token from environment variables
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        raise ValueError("No TELEGRAM_TOKEN found in environment variables")

    # Create the application instance
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()