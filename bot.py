import telebot
import requests
import json

# Replace with your Telegram Bot Token from @BotFather
BOT_TOKEN = "6045936754:AAFnmUzK2h59YPGTdx9Ak6oIWPvh1oST_KU"

# Primary TikTok API (replace with an actual working API)
TIKTOK_API_URL = "https://api.sumiproject.net/tiktok?video={}"

# Alternative API if the first one fails (example: ssstik.io API)
ALT_TIKTOK_API_URL = "https://ssstik.io/api/get?url={}"

# Optional: If the API requires an API key
API_KEY = None  # Replace with your API key if needed

# Custom headers (if needed to bypass 403 restrictions)
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

    # Try the first API
    video_url = fetch_tiktok_url(video_link, TIKTOK_API_URL)
    
    # If the first API fails, try an alternative API
    if not video_url:
        video_url = fetch_tiktok_url(video_link, ALT_TIKTOK_API_URL)

    # Send the result to the user
    if video_url:
        bot.reply_to(message, f"🎥 Here is your playable TikTok video link:\n🔗 {video_url}")
    else:
        bot.reply_to(message, "⚠️ Failed to fetch the video link. Try another TikTok video.")

def fetch_tiktok_url(video_link, api_url):
    """
    Fetch the TikTok video URL from the given API.
    """
    try:
        # Construct API request
        full_url = api_url.format(video_link)
        if API_KEY:
            full_url += f"&key={API_KEY}"

        response = requests.get(full_url, headers=HEADERS)

        # Debugging: Print API request and response for better insights
        print(f"API Request URL: {full_url}")
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Text: {response.text}")

        # Check if the request was successful
        if response.status_code == 200:
            try:
                data = response.json()
                print("API Response JSON:", data)  # Debugging: print raw response data
                return data.get("url")  # Extract the video URL if available
            except json.JSONDecodeError:
                print("⚠️ Error decoding API response: Non-JSON response.")
                return None

        elif response.status_code == 403:
            print("❌ API returned 403 Forbidden. The API might require an API key or be blocked.")
            return None

        else:
            print(f"❌ API request failed. Status Code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {str(e)}")
        return None

# Start the bot
bot.polling()