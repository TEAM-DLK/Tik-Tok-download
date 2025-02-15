# bot.py

import os
import uuid
import shutil
import requests
from config import API_HASH, APP_ID, BOT_TOKEN, DOWNLOADS_DIR
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Initialize the bot client
bot = Client(
    'Tik-Tok-download',
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Inline Keyboard Buttons
START_BUTTONS = [
    [
        InlineKeyboardButton("Source", url="https://github.com/TEAM-DLK/Tik-Tok-download"),
        InlineKeyboardButton("Project Channel", url="https://t.me/DOOZY_OFF"),
    ],
    [InlineKeyboardButton("Author", url="http://t.me/iiiIiiiAiiiMiii")],
]

DL_BUTTONS = [
    [
        InlineKeyboardButton("No Watermark", callback_data="nowm"),
        InlineKeyboardButton("Watermark", callback_data="wm"),
    ],
    [InlineKeyboardButton("Audio", callback_data="audio")],
]

# Start command handler
@bot.on_message(filters.command('start') & filters.group)
async def start(bot, update):
    await update.reply_text(
        "I'm Tik-Tok-download!\nYou can download TikTok videos or audio using this bot.",
        reply_markup=InlineKeyboardMarkup(START_BUTTONS)
    )

# Message handler for TikTok URLs
@bot.on_message(filters.regex(r'http.*') & filters.group)
async def tiktok_handler(bot, update):
    url = update.text
    session = requests.Session()
    try:
        resp = session.head(url, allow_redirects=True)
        if 'tiktok.com' not in resp.url:
            return
        await update.reply(
            'Select download option:',
            reply_markup=InlineKeyboardMarkup(DL_BUTTONS)
        )
    except Exception as e:
        await update.reply_text(f"Error validating URL: {str(e)}")

# Callback query handler
@bot.on_callback_query()
async def callback_handler(bot, cb: CallbackQuery):
    try:
        if cb.data not in ['nowm', 'wm', 'audio']:
            return

        # Create unique temp directory
        dir_id = uuid.uuid4().hex
        temp_dir = os.path.join(DOWNLOADS_DIR, dir_id)
        os.makedirs(temp_dir, exist_ok=True)

        update = cb.message.reply_to_message
        await cb.message.delete()
        url = update.text

        # Resolve final URL
        with requests.Session() as session:
            resp = session.head(url, allow_redirects=True)
            clean_url = resp.url.split('?', 1)[0] if '?' in resp.url else resp.url
            video_id = clean_url.split('/')[-1].split('?')[0]
            
            # Fetch TikTok metadata
            api_response = session.get(
                f'https://subhatde.id.vn/tiktok/downloadvideo?={clean_url}'
            )
            api_response.raise_for_status()
            data = api_response.json()

            # Download selected media
            media_url = data['result'][cb.data]
            media_response = session.get(media_url, stream=True)
            media_response.raise_for_status()

            file_path = os.path.join(temp_dir, f"{video_id}.mp4")
            with open(file_path, 'wb') as f:
                for chunk in media_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            # Handle different media types
            if cb.data in ['nowm', 'wm']:
                await bot.send_video(
                    chat_id=update.chat.id,
                    video=file_path,
                    caption="Downloaded via @YourBot"
                )
            elif cb.data == 'audio':
                audio_path = os.path.join(temp_dir, f"{video_id}.mp3")
                os.system(
                    f'ffmpeg -i "{file_path}" -vn -ar 44100 -ac 2 -ab 192k "{audio_path}"'
                )
                await bot.send_audio(
                    chat_id=update.chat.id,
                    audio=audio_path
                )

    except requests.exceptions.RequestException as e:
        await cb.message.reply_text(f"API Error: {str(e)}")
    except KeyError:
        await cb.message.reply_text("Invalid API response format")
    except Exception as e:
        await cb.message.reply_text(f"Unexpected error: {str(e)}")
    finally:
        # Cleanup temp files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    import asyncio
    print("Bot starting...")
    
    # Start Pyrogram client
    async def main():
        await bot.start()
        print("Bot started successfully!")
        # Keep the process alive
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(bot.stop())
        print("Bot stopped")