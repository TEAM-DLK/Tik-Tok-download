import json
import telebot
import requests

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = "6045936754:AAEwmk2cNv19VSxEcKr4NaMjCNRk5I5AiZI"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# TikTok Video URL
video_url = "https://vt.tiktok.com/ZSMY2qVS5/"  # Replace with your TikTok URL

# Fetch TikTok Data from API
TIKTOK_API_URL = f"https://api.sumiproject.net/tiktok?video={video_url}"

# Fetch the API data
response = requests.get(TIKTOK_API_URL)

# Check if the response is successful
if response.status_code != 200:
    print(f"Error: Failed to fetch data. Status code: {response.status_code}")
    exit()

# Load the API response as JSON
data = response.json()

# Check if 'data' key exists in the response
if "data" not in data:
    print("Error: Invalid API response. 'data' key not found.")
    exit()

# Extract video details from the API response
video_data = data["data"]
video_url = video_data.get("play", None)  # Get video URL safely
title = video_data.get("title", "No Title")
author = video_data.get("author", {}).get("nickname", "Unknown")
avatar = video_data.get("author", {}).get("avatar", "")
cover = video_data.get("cover", "")
likes = video_data.get("digg_count", 0)
shares = video_data.get("share_count", 0)
comments = video_data.get("comment_count", 0)
views = video_data.get("play_count", 0)

# Check if video URL exists
if not video_url:
    print("Error: No video URL found in API response.")
    exit()

# Telegram chat ID where you want to send the video
CHAT_ID = "-1001986456136"  # Replace with actual chat ID

# Video caption
caption = (
    f"🎵 *{title}*\n"
    f"👤 Tác giả: {author}\n"
    f"👁 Lượt xem: {views:,}\n"
    f"❤️ Lượt thích: {likes:,}\n"
    f"💬 Bình luận: {comments:,}\n"
    f"🔗 [Xem trên TikTok]({video_url})"
)

# Send the video to Telegram
try:
    bot.send_video(CHAT_ID, video_url, caption=caption, parse_mode="Markdown")
    print("✅ Video sent successfully!")
except Exception as e:
    print(f"Error sending video: {e}")