import logging
import requests
import json
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram bot token (Replace with your bot token)
TOKEN = "6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU"

# API URL
API_URL = "https://subhatde.id.vn/tiktok/downloadvideo?url={}"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a TikTok video link, and I'll fetch the download link for you!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text

    if "tiktok.com" not in user_text:
        await update.message.reply_text("Please send a valid TikTok video link.")
        return

    # Call API
    response = requests.get(API_URL.format(user_text))
    
    if response.status_code == 200:
        try:
            # Extract JSON from HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            json_text = soup.find("pre").text
            data = json.loads(json_text)

            # Check if response contains video data
            if data.get("code") == 0 and "data" in data:
                video_data = data["data"]
                title = video_data.get("title", "No Title")
                video_url = video_data.get("play", "No Video Link")
                music_url = video_data.get("music", "No Music Link")

                # Send response to user
                message = f"🎬 *Video Title:* {title}\n\n📥 *Download Video:* [Click Here]({video_url})\n🎵 *Music:* [Click Here]({music_url})"
                await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            else:
                await update.message.reply_text("Failed to retrieve video data. Please try again.")
        
        except Exception as e:
            await update.message.reply_text("Error processing response. Please try again.")
            logging.error(f"Error: {e}")

    else:
        await update.message.reply_text("Failed to fetch video. Please try again.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()