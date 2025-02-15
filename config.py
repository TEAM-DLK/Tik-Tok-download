import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the bot token from environment variables
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')