import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a TikTok video URL to download.')

def download_video(update: Update, context: CallbackContext) -> None:
    url = 'https://subhatde.id.vn/tiktok/downloadvideo?url=' + context.args[0]
    response = requests.get(url)
    if response.status_code == 200:
        video_url = response.json().get('video_url')
        update.message.reply_text(f'Video URL: {video_url}')
    else:
        update.message.reply_text('Failed to retrieve video.')

def main() -> None:
    updater = Updater(os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('download', download_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()