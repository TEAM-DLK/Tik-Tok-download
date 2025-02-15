import telebot
import requests

# Replace with your Telegram Bot Token from @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Alternative API (ssstik.io)
TIKTOK_API_URL = "https://ssstik.io/api/get?url={}"

# Custom headers to prevent bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Initialize the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎥 Send me a TikTok video link, and I'll get the direct play URL for you!")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def get_playable_link(message):
    video_link = message.text.strip()

    # Fetch the video URL using ssstik.io
    video_url = fetch_tiktok_url(video_link, TIKTOK_API_URL)

    # If the API request fails, notify the user
    if video_url:
        bot.reply_to(message, f"🎥 Here is your TikTok video link:\n🔗 {video_url}")
    else:
        bot.reply_to(message, "⚠️ Failed to fetch the video. Try another link.")

def fetch_tiktok_url(video_link, api_url):
    """
    Fetch the TikTok video URL from the given API.
    """
    try:
        full_url = api_url.format(video_link)
        response = requests.get(full_url, headers=HEADERS)

        print(f"API Request: {full_url}")  # Debugging
        print(f"API Response Code: {response.status_code}")
        print(f"API Response Text: {response.text}")

        # Check if the API response is valid
        if response.status_code == 200:
            data = response.json()
            return data.get("url")

        elif response.status_code == 404:
            print("❌ API returned 404 Not Found. The endpoint may be broken.")
            return None

        else:
            print(f"❌ API failed with status {response.status_code}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {str(e)}")
        return None

# Start the bot
bot.polling()