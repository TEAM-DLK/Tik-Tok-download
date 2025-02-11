# app.py

import os
import uuid
import shutil
import requests
from config import API_HASH, APP_ID, BOT_TOKEN, DOWNLOADS_DIR
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Initialize the bot client
bot = Client('Tik-Tok-download', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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
        True,
        reply_markup=InlineKeyboardMarkup(START_BUTTONS)
    )

# Message handler for TikTok URLs
@bot.on_message(filters.regex(pattern='.*http.*') & filters.group)
async def tiktok(bot, update):
    url = update.text
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    if 'tiktok.com' not in resp.url:
        return
    await update.reply('Select the options below', True, reply_markup=InlineKeyboardMarkup(DL_BUTTONS))

# Callback query handler
@bot.on_callback_query()
async def callbacks(bot, cb: CallbackQuery):
    if cb.data in ['nowm', 'wm', 'audio']:
        dirs = DOWNLOADS_DIR.format(uuid.uuid4().hex)
        os.makedirs(dirs)
        update = cb.message.reply_to_message
        await cb.message.delete()
        url = update.text
        session = requests.Session()
        resp = session.head(url, allow_redirects=True)
        tt = resp.url.split('?', 1)[0] if '?' in resp.url else resp.url
        ttid = dirs + tt.split('/')[-1]
        r = requests.get(f'https://api.reiyuura.me/api/dl/tiktok?url={tt}')
        result = r.text
        rs = result.json()
        link = rs['result'][cb.data]
        resp = session.head(link, allow_redirects=True)
        r = requests.get(resp.url, allow_redirects=True)
        with open(f'{ttid}.mp4', 'wb') as f:
            f.write(r.content)
        if cb.data == 'nowm':
            await bot.send_video(update.chat.id, f'{ttid}.mp4')
        elif cb.data == 'wm':
            await bot.send_video(update.chat.id, f'{ttid}.mp4')
        elif cb.data == 'audio':
            cmd = f'ffmpeg -i "{ttid}.mp4" -vn -ar 44100 -ac 2 -ab 192 -f mp3 "{ttid}.mp3"'
            os.system(cmd)
            await bot.send_audio(update.chat.id, f'{ttid}.mp3')
        shutil.rmtree(dirs)

# Run the bot
bot.run()