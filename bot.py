import telebot
import requests
import json

# Telegram Bot Token from BotFather
BOT_TOKEN = "6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU"

# TikTok API URL
TIKTOK_API_URL = "https://api.sumiproject.net/tiktok?video={}"

# Custom headers (if required)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send me a TikTok video link, and I'll get the direct play URL for you!")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def get_playable_link(message):
    video_link = message.text.strip()

    try:
        # Request video URL from API with headers
        response = requests.get(TIKTOK_API_URL.format(video_link), headers=HEADERS)

        # Debugging: Print API response
        print("API Response:", response.text)

        # Check response status
        if response.status_code == 200:
            data = response.json()
            video_url = data.get("url")

            if video_url:
                bot.reply_to(message, f"🎥 Here is your playable TikTok video link:\n🔗 {video_url}")
            else:
                bot.reply_to(message, "⚠️ The API did not return a valid video link. Please check your TikTok URL.")

        elif response.status_code == 403:
            bot.reply_to(message, "❌ API returned 403 Forbidden. The API might require an API key or be blocked.")

        else:
            bot.reply_to(message, f"❌ API request failed. Status Code: {response.status_code}")

    except json.JSONDecodeError:
        bot.reply_to(message, "⚠️ Error decoding API response. The API might be down.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"🚨 Network error: {str(e)}")

# Start the bot
bot.polling()