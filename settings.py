import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv('BOT_TOKEN')
TEAM_CHAT = os.getenv('TEAM_CHAT')
GAME_ADMIN = os.getenv('GAME_ADMIN')
STOP_WORD = os.getenv('STOP_WORD', '#анонс')
TEAM_NAME = os.getenv('TEAM_NAME')

# Validate all required settings
if not TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")

if not TEAM_CHAT:
    raise ValueError("TEAM_CHAT is not set in environment variables")

if not GAME_ADMIN:
    raise ValueError("GAME_ADMIN is not set in environment variables")

if not TEAM_NAME:
    raise ValueError("TEAM_NAME is not set in environment variables")

# Convert numeric values (Telegram chat IDs are integers)
try:
    TEAM_CHAT = int(TEAM_CHAT)
except (ValueError, TypeError):
    raise ValueError("TEAM_CHAT must be a valid integer")

try:
    GAME_ADMIN = int(GAME_ADMIN)
except (ValueError, TypeError):
    raise ValueError("GAME_ADMIN must be a valid integer")