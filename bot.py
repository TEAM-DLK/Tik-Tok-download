import logging
import os
import requests
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the function to get the TikTok video
def get_tiktok_video(video_url):
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_id or not api_hash:
        logger.error("API_ID or API_HASH not found in environment variables!")
        return None

    params = {
        "video": video_url,
        "api_id": api_id,
        "api_hash": api_hash
    }

    api_url = "https://api.sumiproject.net/tiktok"
    try:
        response = requests.get(api_url, params=params, timeout=10)  # Add timeout
        response.raise_for_status()  # Raise error if the request failed

        data = response.json()
        logger.info(f"API response: {data}")  # Log response for debugging

        return data.get("download_url")

    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        return None
    except ValueError:
        logger.error(f"Error parsing JSON response: {response.text}")
        return None

# Start Command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! Send me a TikTok video link, and I will download it for you.")

# Function to handle video link
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if "tiktok.com" in text:  # Simple validation for TikTok links
        await update.message.reply_text("Fetching your TikTok video... Please wait.")
        
        # Run the API call in a separate thread to avoid blocking
        download_url = await asyncio.to_thread(get_tiktok_video, text)

        if download_url:
            await update.message.reply_text(f"Your TikTok video download link: {download_url}")
        else:
            await update.message.reply_text("Sorry, I couldn't fetch the video. Please try again later.")
    else:
        await update.message.reply_text("Please send a valid TikTok video link.")

def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        raise ValueError("No TELEGRAM_TOKEN found in environment variables")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()