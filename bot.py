import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TELEGRAM_API_TOKEN = '6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU'

# Function to get the TikTok video without watermark
def get_tiktok_video(link: str) -> str:
    api_url = f"https://tikcd.com/api/v1/tiktok?url={link}&no_watermark=true"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("download_url", "Failed to get the download URL.")
    return "Failed to download the video."

# Command to start bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me a TikTok link, and I will fetch the video without a watermark.')

# Function to handle received messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if "tiktok.com" in text:
        video_url = get_tiktok_video(text)
        await update.message.reply_text(f"Here is your video: {video_url}")
    else:
        await update.message.reply_text("Please send a valid TikTok link.")

# Main function to run the bot
def main() -> None:
    # Create the application and pass the bot token
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Adding command handlers
    application.add_handler(CommandHandler("start", start))

    # Adding message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling the bot
    application.run_polling()

if __name__ == '__main__':
    main()