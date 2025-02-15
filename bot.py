import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TELEGRAM_API_TOKEN = '6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU'

# Function to get the TikTok video without watermark, HD, or MP3
def get_tiktok_video(link: str, download_type="no_watermark") -> str:
    # Map the download type to the corresponding API parameter
    download_types = {
        "no_watermark": "no_watermark=true",
        "no_watermark_hd": "no_watermark=true&quality=hd",
        "mp3": "mp3=true",
        "other": ""  # Add other specific parameters if needed
    }

    # Get the correct parameter for the download type
    download_param = download_types.get(download_type, "no_watermark=true")  # Default to 'no_watermark'

    api_url = f"https://tikcd.com/api/v1/tiktok?url={link}&{download_param}"

    try:
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            if "download_url" in data:
                return data["download_url"]
            else:
                return f"Error: No download URL found in the response. Response: {data}"
        else:
            return f"Error: Received an unexpected status code {response.status_code}. Response: {response.text}"

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        return f"Error: A problem occurred while making the request. Details: {e}"

# Command to start bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me a TikTok link, and I will fetch the video for you. You can also request "HD" or "MP3".')

# Function to handle received messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if "tiktok.com" in text:
        # Default to "no_watermark"
        download_type = "no_watermark"

        # Check if the user has specified a type, like "HD" or "MP3"
        if "HD" in text:
            download_type = "no_watermark_hd"
        elif "MP3" in text:
            download_type = "mp3"

        video_url = get_tiktok_video(text, download_type)
        await update.message.reply_text(f"Here is your {download_type} video: {video_url}")
    else:
        await update.message.reply_text("Please send a valid TikTok link.")

# Main function to run the bot
def main() -> None:
    # Create the application and pass the bot token
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Adding command handlers
    application.add_handler(CommandHandler("start", start))

    # Adding message handler to handle received TikTok links
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling the bot
    application.run_polling()

if __name__ == '__main__':
    main()