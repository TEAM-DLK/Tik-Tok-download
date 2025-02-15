import logging
import requests
import json
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram bot token (Replace with your actual token)
TOKEN = "6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU"

# API URL for fetching the play link
API_URL = "https://subhatde.id.vn/tiktok/play?url={}"  # Make sure this is the correct API

# Headers to avoid request blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a TikTok video link, and I'll fetch the play link for you!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text

    if "tiktok.com" not in user_text:
        await update.message.reply_text("❌ Please send a valid TikTok video link.")
        return

    # Call API with headers
    response = requests.get(API_URL.format(user_text), headers=headers)
    
    if response.status_code == 200:
        try:
            # Extract JSON from API response (Remove HTML tags)
            json_text = re.search(r'<pre.*?>(.*?)</pre>', response.text, re.DOTALL).group(1)
            data = json.loads(json_text)

            # Check if response contains video data
            if data.get("code") == 0 and "data" in data:
                video_data = data["data"]
                play_url = video_data.get("play", "No Play Link Available")

                # Send play link to user
                await update.message.reply_text(f"▶️ *Play Link:* [Click Here]({play_url})", parse_mode="Markdown", disable_web_page_preview=True)
            else:
                await update.message.reply_text("⚠️ Failed to retrieve play link. Please try again.")
        
        except Exception as e:
            await update.message.reply_text("⚠️ Error processing response. Please try again.")
            logging.error(f"Error: {e}")

    else:
        await update.message.reply_text(f"⚠️ API Error: {response.status_code}. Check API.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()