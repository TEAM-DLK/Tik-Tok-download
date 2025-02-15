import os
import uuid
import shutil
import requests
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from requests.exceptions import RequestException
from config import API_ID, API_HASH, BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot client
bot = Client(
    'tiktok_downloader_bot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Inline Keyboard Buttons
START_BUTTONS = [
    [
        InlineKeyboardButton("Source Code", url="https://github.com/YourUsername/tiktok_downloader_bot"),
        InlineKeyboardButton("Author", url="https://t.me/YourTelegramUsername"),
    ],
]

DL_BUTTONS = [
    [
        InlineKeyboardButton("No Watermark", callback_data="nowm"),
        InlineKeyboardButton("Watermark", callback_data="wm"),
    ],
    [InlineKeyboardButton("Audio", callback_data="audio")],
]

# Start command handler
@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply_text(
        "Hello! I'm a TikTok Downloader Bot.\n"
        "Send me a TikTok video link, and I'll download it for you.",
        reply_markup=InlineKeyboardMarkup(START_BUTTONS)
    )

# Message handler for TikTok URLs
@bot.on_message(filters.regex(r'https?://(?:www\.)?tiktok\.com/.+') & filters.private)
async def tiktok_handler(bot, message):
    url = message.text.strip()
    await message.reply(
        'Choose download option:',
        reply_markup=InlineKeyboardMarkup(DL_BUTTONS)
    )

# Callback query handler
@bot.on_callback_query()
async def callback_handler(bot, callback_query: CallbackQuery):
    data = callback_query.data
    message = callback_query.message
    user_message = message.reply_to_message

    if data not in ['nowm', 'wm', 'audio']:
        return

    url = user_message.text.strip()
    temp_dir = '/tmp'  # Use Heroku's temp directory
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Fetch TikTok video data
        api_url = f'https://subhatde.id.vn/tiktok/downloadvideo?url={url}'
        response = requests.get(api_url, timeout=30)  # Set a 30-second timeout
        response.raise_for_status()
        video_data = response.json()

        if data == 'nowm':
            download_url = video_data['nowatermark']
        elif data == 'wm':
            download_url = video_data['watermark']
        else:
            download_url = video_data['audio']

        # Download the media
        media_response = requests.get(download_url, stream=True, timeout=30)  # Timeout for media download
        media_response.raise_for_status()

        file_extension = 'mp4' if data != 'audio' else 'mp3'
        file_path = os.path.join(temp_dir, f"tiktok_media.{file_extension}")

        with open(file_path, 'wb') as f:
            for chunk in media_response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Send the media to the user
        if data == 'audio':
            await bot.send_audio(chat_id=user_message.chat.id, audio=file_path)
        else:
            await bot.send_video(chat_id=user_message.chat.id, video=file_path)

    except RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        await message.reply_text(f"An error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        await message.reply_text(f"An unexpected error occurred: {str(e)}")
    finally:
        # Cleanup the temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    bot.run()