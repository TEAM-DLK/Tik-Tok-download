import telebot
import requests
import json

# Replace with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = "6045936754:AAEwmk2cNv19VSxEcKr4NaMjCNRk5I5AiZI"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# TikTok API URL (No API key needed)
TIKTOK_API_URL = "https://api.sumiproject.net/tiktok?video={}"

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Send me a TikTok video link, and I'll fetch it for you!")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def fetch_tiktok_video(message):
    tiktok_url = message.text.strip()
    api_url = TIKTOK_API_URL.format(tiktok_url)

    headers = {"User-Agent": "Mozilla/5.0"}  # Helps prevent API request blocks
    
    try:
        response = requests.get(api_url, headers=headers)

        # Debugging: Print raw API response
        print("Raw API Response:", response.text)

        # Ensure response is valid JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            bot.reply_to(message, "Error: API did not return valid JSON.")
            return

        # Check if 'data' and 'play' keys exist
        if "data" not in data or "play" not in data["data"]:
            bot.reply_to(message, "Error: Could not find video URL in API response.")
            return

        video_url = data["data"]["play"]  # Extract video URL without watermark

        # Send the video to Telegram
        bot.send_video(message.chat.id, video_url, caption="Here is your TikTok video!")

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Error fetching video data: {str(e)}")

bot.polling()