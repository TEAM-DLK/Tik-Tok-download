import telebot
import requests

# Telegram Bot Token from BotFather
BOT_TOKEN = "6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU"

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# TikTok API URL
TIKTOK_API_URL = "https://api.sumiproject.net/tiktok?video={}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send me a TikTok video link, and I'll get the direct play URL for you!")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def get_playable_link(message):
    video_link = message.text.strip()
    
    try:
        # Fetch the direct video URL from the API
        response = requests.get(TIKTOK_API_URL.format(video_link))
        if response.status_code == 200:
            data = response.json()
            video_url = data.get("url")  # API should return direct video URL

            if video_url:
                bot.reply_to(message, f"Here is your playable TikTok video link:\n{video_url}")
            else:
                bot.reply_to(message, "Failed to get the video link. Try another video.")

        else:
            bot.reply_to(message, "Error fetching video. Please try again.")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Start the bot
bot.polling()