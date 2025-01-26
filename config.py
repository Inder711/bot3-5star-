#(©)CodeXBotz

import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant

load_dotenv()

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "23929647"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "b9afa697042d998a758e407b84c86daf")

# Your db channel ID
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002401143074"))

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "5176888500"))

# Port
PORT = os.environ.get("PORT", "8080")

# Database
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://5starbot123:7ipeSH1moZfrUzDf@cluster0.wa0so.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# Force subscription channel IDs
FORCE_SUB_CHANNEL = [
    int(channel_id.strip()) for channel_id in os.environ.get("FORCE_SUB_CHANNEL", "-1002424794894,-1002489269478").split(",")
]

JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", None)

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start message
START_PIC = os.environ.get("START_PIC", "")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")

try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "5176888500").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Force subscription message
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

# Set your custom caption here, Keep None to disable custom caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Auto delete time in seconds
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "0"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "Your file has been successfully deleted. Thank you for using our service. ✅")

# Set true if you want to disable your channel posts share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)
ADMINS.append(5176888500)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

# Initialize Pyrogram Client
app = Client(
    "ForceSubBot",
    bot_token=TG_BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH
)

# Check if a user is subscribed to a specific channel
def is_subscribed(client, user_id, channel_id):
    try:
        member = client.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except UserNotParticipant:
        return False
    except Exception as e:
        LOGGER("ForceSub").warning(f"Error checking subscription for channel {channel_id}: {e}")
        return False

# Check if a user is subscribed to all required channels
def check_subscription(client, user_id):
    not_subscribed = []
    for channel_id in FORCE_SUB_CHANNEL:
        if not is_subscribed(client, user_id, channel_id):
            not_subscribed.append(channel_id)
    return not_subscribed

# Handle /start command
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    unsubscribed_channels = check_subscription(client, user_id)

    if unsubscribed_channels:
        message_text = "Hello {first},\n\n<b>You need to join the following channels to use this bot:</b>\n\n".format(first=message.from_user.first_name)
        for channel_id in unsubscribed_channels:
            invite_link = await client.export_chat_invite_link(channel_id)
            message_text += f"👉 <a href='{invite_link}'>Click here to join</a>\n"
        message_text += "\n<b>After joining, click /start to use the bot.</b>"
        await message.reply_text(
            text=message_text,
            disable_web_page_preview=True,
            parse_mode="html"
        )
    else:
        await message.reply_text(
            text=START_MSG.format(first=message.from_user.first_name),
            disable_web_page_preview=True,
            parse_mode="html"
        )

if __name__ == "__main__":
    LOGGER("ForceSubBot").info("Bot started successfully.")
    app.run()
