import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import BOT_TOKEN

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a TikTok video URL to download.')

def download_video(update: Update, context: CallbackContext) -> None:
    if context.args:
        url = f"https://subhatde.id.vn/tiktok/downloadvideo?url={context.args[0]}"
        response = requests.get(url)
        if response.status_code == 200:
            video_url = response.json().get('video_url')
            if video_url:
                update.message.reply_text(f'Video URL: {video_url}')
            else:
                update.message.reply_text('Failed to retrieve video URL.')
        else:
            update.message.reply_text('Error fetching video.')
    else:
        update.message.reply_text('Please provide a TikTok video URL.')

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('download', download_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()