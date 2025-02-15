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
    bot.reply_to(message, "Send me a TikTok video link, and I'll download it for you!")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download_tiktok_video(message):
    video_link = message.text.strip()
    
    try:
        # Fetch the video URL from the API
        response = requests.get(TIKTOK_API_URL.format(video_link))
        if response.status_code == 200:
            video_url = response.json().get("url")  # Ensure API returns "url"

            # Download the video
            video_data = requests.get(video_url).content
            with open("tiktok_video.mp4", "wb") as video_file:
                video_file.write(video_data)

            # Send the video to the user
            with open("tiktok_video.mp4", "rb") as video_file:
                bot.send_video(message.chat.id, video_file, caption="Here is your TikTok video!")

        else:
            bot.reply_to(message, "Failed to fetch video. Try again.")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Start the bot
bot.polling()