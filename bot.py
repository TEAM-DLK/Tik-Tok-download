import telebot
import requests

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = "6045936754:AAEwmk2cNv19VSxEcKr4NaMjCNRk5I5AiZI"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

TIKTOK_API_URL = "https://api.sumiproject.net/tiktok?video={}"

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Send me a TikTok video link!")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def fetch_tiktok_video(message):
    tiktok_url = message.text.strip()
    api_url = TIKTOK_API_URL.format(tiktok_url)

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json().get("data", {})

        if data:
            video_url = data["play"]  # Extract video URL without watermark

            # Send video without any caption
            bot.send_video(message.chat.id, video_url)
        else:
            bot.reply_to(message, "Failed to fetch video. Try another link.")
    else:
        bot.reply_to(message, "Error fetching video data. Please try again.")

bot.polling()