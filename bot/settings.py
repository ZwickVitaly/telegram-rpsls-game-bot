import os
from os import getenv
from loguru import logger


# Set DEBUG for sqlite database and advanced logging
DEBUG = os.getenv("DEBUG", "0") == "1"

# logging configure
logger.add(
    'logs/debug_logs.log' if DEBUG else 'logs/bot.log',
    rotation="00:00:00",
    level="DEBUG" if DEBUG else "INFO",
)

# Set if only bot will work in groups only
GROUP_ONLY = os.getenv("GROUP_ONLY_BOT", "1") == "1"

# Get bot token at @BotFather
BOT_TOKEN = getenv("BOT_TOKEN")


# Set databases
DATABASES = {
    # Configured only for POSTGRESQL
    "main": {
        "username": getenv("POSTGRES_USER"),
        "password": getenv("POSTGRES_PASSWORD"),
        "host": getenv("POSTGRES_HOST"),
        "port": getenv("POSTGRES_PORT"),
        "db_name": getenv("POSTGRES_DB"),
        "default_user_name": "admin",
        "driver": "postgresql+asyncpg"
    },
    # Configured only for SQLITE
    "debug": {
        "path": "database.db",
        "driver": "sqlite+aiosqlite"
    }
}


# Set True if you want webhook bot. Don't forget to edit variables down below
WEBHOOK_DISPATCHER = getenv("WEBHOOKS", "0") == "1"

# Secret key to verify telegram messages
WEBHOOK_SECRET_TOKEN = getenv("WEBHOOK_SECRET_TOKEN")


# Web server host. better "0.0.0.0" if used in container
WEB_SERVER_HOST = "0.0.0.0"

# Choose any, don't go 80 or 443 :)
WEB_SERVER_PORT = int(getenv("WEBHOOK_PORT")) or 8080


# Path to your webhook for Telegram server
# Base format - http://yourpath_OR_ip
# Path format - /webhook
# If you want webhook bot - better configure hooks right, or it will fall apart :)
BASE_WEBHOOK_URL = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")

# Register user command
REGISTER_COMMAND = "/register"

NGINX_STATIC = os.getenv("NGINX_STATIC") == "1"

# Static dir
if NGINX_STATIC:
    STATIC_PATH = f"{os.getenv('WEBHOOK_HOST')}/static/"
else:
    STATIC_PATH = "static/"

# Throttle timer value in seconds.
# MUST BE ABOVE ZERO
THROTTLE_TIMER = 5

# Throttle rate value (how many requests per THROTTLE_TIMER bot will accept from user)
# MUST BE ABOVE ZERO
THROTTLE_RATE = 5

# Throttle timeout
# If lower than 1 - will be = THROTTLE_TIMER
THROTTLE_TIMEOUT = 30


# Only group bot reply to private message
BOT_OWNER = os.getenv("BOT_OWNER") or ""
logger.info(f"Bot owner: {BOT_OWNER}")
BOT_OWNER_MESSAGE = f"\n{'Чтобы добавить бота себе в чат напиши ' if BOT_OWNER else ''} {BOT_OWNER}"\
    if BOT_OWNER else ''


# Redis game index name
RPSLS_GAME_INDEX_KEY = "rpsls_game_index"

# RPSLS Command
RPSLS_START_COMMAND = "/start_rpsls"

# Game start waiting time and round time in seconds
RPSLS_GAME_START_TIMER = 300
RPSLS_GAME_ROUND_TIMER = 150
