# ============================================================
# config.py — SMS Campaign Manager Bot Configuration
# ============================================================

# Telegram Bot Token (from @BotFather)
BOT_TOKEN = "8665622616:AAGu_Ns2vsXAPwYf9-WESg7DGi_9AoKyshs"

# No default Firebase — each user adds their own via the bot

# Default delay in seconds between SMS dispatches per device
DEFAULT_SMS_DELAY = 2.0

# Admin Telegram IDs — these users get access to Admin Panel
# Example: [123456789, 987654321]
ADMIN_IDS = [5989102250]

# Authorized User IDs — empty list = allow everyone
# Example: [123456789] = only this user can use the bot
AUTHORIZED_USERS = []

# Max targets per campaign
MAX_TARGETS_PER_CAMPAIGN = 10000

# SQLite database path
DB_PATH = "sms_bot.db"

# Campaign ID prefix
CAMPAIGN_PREFIX = "CMP"
