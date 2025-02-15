import telebot
import requests

# ✅ Replace with your actual Telegram Bot Token
BOT_TOKEN = "6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU"

# ✅ New working API for TikTok video download (no watermark)
TIKTOK_API_URL = "https://tikcdn.io/api/download/{}/noWatermark"

# Custom headers to prevent bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Initialize Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎥 Send me a TikTok video link, and I'll fetch the direct download link for you!")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def get_playable_link(message):
    video_link = message.text.strip()

    # Resolve TikTok short links (vt.tiktok.com)
    final_url = resolve_tiktok_redirect(video_link)

    # Fetch the video URL using the API
    video_url = fetch_tiktok_url(final_url, TIKTOK_API_URL)

    # If successful, send the video URL
    if video_url:
        bot.reply_to(message, f"🎥 Here is your TikTok video:\n🔗 {video_url}")
    else:
        bot.reply_to(message, "⚠️ Failed to fetch the video. Try another link.")

def resolve_tiktok_redirect(url):
    """
    Resolves TikTok short links (vt.tiktok.com) to final URL.
    """
    try:
        response = requests.get(url, headers=HEADERS, allow_redirects=True)
        return response.url  # Returns the final TikTok video URL
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error resolving redirect: {str(e)}")
        return url  # If error, return the original link

def fetch_tiktok_url(video_link, api_url):
    """
    Fetch the TikTok video URL from an alternative API.
    """
    try:
        full_url = api_url.format(video_link)
        response = requests.get(full_url, headers=HEADERS)

        print(f"🔍 API Request: {full_url}")
        print(f"🔍 API Response Code: {response.status_code}")
        print(f"🔍 API Response Text: {response.text}")  # Debugging

        # Check if the API response is valid
        if response.status_code == 200:
            data = response.json()
            return data.get("video")  # Adjust based on the actual API response

        print("❌ API returned an error.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {str(e)}")
        return None

# Start the bot
bot.polling()