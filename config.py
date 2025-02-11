# config.py

import os

# Retrieve sensitive information from environment variables
API_HASH = os.getenv('API_HASH')
APP_ID = int(os.getenv('APP_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Define the download directory template
DOWNLOADS_DIR = './downloads/{}/'
