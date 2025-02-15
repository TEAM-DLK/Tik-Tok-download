import telebot
import requests

# Replace with your Telegram Bot Token from @BotFather
BOT_TOKEN = "6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU"

# TikCD API URL
TIKCD_API_URL = "https://tikcd.com/api/video?url={}"

# Custom headers to avoid bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Initialize the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎥 Send me a TikTok video link, and I'll download it for you!")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download_tiktok_video(message):
    video_link = message.text.strip()

    # Fetch the TikTok video URL using TikCD API
    video_url = fetch_tiktok_url(video_link)

    # If successful, download and send the video
    if video_url:
        bot.send_message(message.chat.id, "🔄 Downloading video...")
        send_video_to_telegram(message.chat.id, video_url)
    else:
        bot.reply_to(message, "⚠️ Failed to fetch the video. Try another link.")

def fetch_tiktok_url(video_link):
    """
    Fetch the TikTok video URL from TikCD API.
    """
    try:
        api_url = TIKCD_API_URL.format(video_link)
        response = requests.get(api_url, headers=HEADERS)
        print(f"🔍 API Request: {api_url}")
        print(f"🔍 API Response Code: {response.status_code}")
        print(f"🔍 API Response Text: {response.text}")  # Debugging

        if response.status_code == 200:
            data = response.json()
            return data.get("video_url")  # Adjust based on the API response

        print("❌ API returned an error.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {str(e)}")
        return None

def send_video_to_telegram(chat_id, video_url):
    """
    Download and send the TikTok video to Telegram.
    """
    try:
        video_data = requests.get(video_url, headers=HEADERS).content
        bot.send_video(chat_id, video_data, caption="🎥 Here is your TikTok video!")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Failed to send video. Error: {str(e)}")

# Start the bot
bot.polling()