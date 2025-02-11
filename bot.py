import json
import os
import shlex
import asyncio
import uuid
import shutil
import requests
from typing import Tuple
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Configs
API_HASH = os.environ['API_HASH']
APP_ID = int(os.environ['APP_ID'])
BOT_TOKEN = os.environ['BOT_TOKEN']
downloads = './downloads/{}/'

# Buttons
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

# Running bot
xbot = Client('Tik-Tok-download', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Helpers
async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

# Start
@xbot.on_message(filters.command('start') & filters.group)
async def _start(bot, update):
    await update.reply_text(f"I'm Tik-Tok-download!\nYou can download TikTok videos/audio using this bot.", True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))

# Downloader for TikTok
@xbot.on_message(filters.regex(pattern='.*http.*') & filters.group)
async def _tiktok(bot, update):
    url = update.text
    if 'tiktok.com' not in url:
        return
    await update.reply('Select the options below', True, reply_markup=InlineKeyboardMarkup(DL_BUTTONS))

# Callbacks
@xbot.on_callback_query()
async def _callbacks(bot, cb: CallbackQuery):
    try:
        dirs = downloads.format(uuid.uuid4().hex)
        os.makedirs(dirs)
        cbb = cb
        update = cbb.message.reply_to_message
        await cb.message.delete()
        url = update.text
        if 'tiktok.com' not in url:
            await cb.message.reply_text("Invalid TikTok URL.")
            return
        session = requests.Session()
        resp = session.get(url, allow_redirects=True)
        final_url = resp.url
        if '?' in final_url:
            tt = final_url.split('?', 1)[0]
        else:
            tt = final_url
        ttid = dirs + tt.split('/')[-1]
        r = requests.get(f'https://api.reiyuura.me/api/dl/tiktok?url={tt}')
        result = r.text
        rs = json.loads(result)
        if cb.data == 'nowm':
            link = rs['result']['nowm']
        elif cb.data == 'wm':
            link = rs['result']['wm']
        elif cb.data == 'audio':
            link = rs['result']['wm']
        else:
            await cb.message.reply_text("Invalid option selected.")
            return
        resp = session.get(link, allow_redirects=True)
        with open(f'{ttid}.mp4', 'wb') as f:
            f.write(resp.content)
        if cb.data == 'audio':
            cmd = f'ffmpeg -i "{ttid}.mp4" -vn -ar 44100 -ac 2 -ab 192 -f mp3 "{ttid}.mp3"'
            await run_cmd(cmd)
            await bot.send_audio(update.chat.id, f'{ttid}.mp3')
            os.remove(f'{ttid}.mp3')
        else:
            await bot.send_video(update.chat.id, f'{ttid}.mp4')
            os.remove(f'{ttid}.mp4')
        shutil.rmtree(dirs)
    except Exception as e:
        await cb.message.reply_text(f"An error occurred: {e}")
        shutil.rmtree(dirs, ignore_errors=True)

xbot.run()