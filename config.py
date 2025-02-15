# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DOWNLOADS_DIR = os.getenv('DOWNLOADS_DIR', '/tmp')

# Ensure all variables are loaded
required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN']
for var in required_vars:
    if not globals().get(var):
        raise ValueError(f"Missing required environment variable: {var}")