import os

# Telegram
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_ADMIN_ID = int(os.environ.get("TG_ADMIN_ID", 0))

# Для Макса (если используем pymax, нужны данные аккаунта)
MAX_PHONE = os.environ.get("MAX_PHONE")
MAX_PASSWORD = os.environ.get("MAX_PASSWORD")
