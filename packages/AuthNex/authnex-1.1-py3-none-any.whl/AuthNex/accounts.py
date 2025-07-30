from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from AuthNex import app
from AuthNex.Database import user_col

SUDO_USER = [6239769036]

@Client.on_message(filters.command('accounts') & (filters.private | filters.group) & filters.user(SUDO_USER), group=10)
async def accounts_handler(_, m: Message):
    count = await user_col.count_documents({})
    if count == 0:
        await m.reply("😭")
        await m.reply("𝗡𝗼 𝗜𝗗'𝗦 𝗳𝗼𝘂𝗻𝗱.") 
        return 

    reply = "🗝 **𝗔𝗹𝗹 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱 𝘂𝘀𝗲𝗿𝘀 𝗹𝗶𝘀𝘁 💳**\n\n"
    
    async for user in user_col.find({}):
        reply += (
            f"**𝗡𝗔𝗠𝗘:** `{user.get('Name', 'N/A')}`\n"
            f"**AGE:** `{user.get('Age', 'N/A')}`\n"
            f"**𝗔𝗨𝗧𝗛-𝗠𝗔𝗜𝗟:** `{user.get('Mail', 'N/A')}`\n" 
            f"**𝗣𝗔𝗦𝗦𝗪𝗢𝗥𝗗:** `{user.get('Password', 'N/A')}`\n"
            f"**AUTH-COINS:** `{user.get('Authcoins', 'N/A')}`\n"
            "----------------------------------\n\n"
        )

    await m.reply(reply, parse_mode=ParseMode.MARKDOWN)
