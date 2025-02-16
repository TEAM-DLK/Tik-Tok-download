import json
import telebot

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = "6045936754:AAEwmk2cNv19VSxEcKr4NaMjCNRk5I5AiZI"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Load TikTok JSON data from file
try:
    with open("tiktok.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: tiktok.json file not found!")
    exit()

# Check if "data" key exists
if "data" not in data:
    print("Error: Invalid JSON format. 'data' key not found.")
    exit()

# Extract video details
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
    print("Error: No video URL found in JSON data.")
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