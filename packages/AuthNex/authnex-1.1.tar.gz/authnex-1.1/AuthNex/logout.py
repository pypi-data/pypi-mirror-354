from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatType
from AuthNex import app
from AuthNex.Database import user_col, sessions_col



@app.on_message(filters.command('logout'), group=7)
async def logout(_, m: Message):
    user_id = m.from_user.id
    session = await sessions_col.find_one({"_id": user_id})
    if not session:
        return await m.reply("💔 𝗡𝗼 𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝗳𝗼𝘂𝗻𝗱 𝗶𝗻 𝗮𝗻𝘆 𝗴𝗺𝗮𝗶𝗹")
    await m.reply("📢 𝗟𝗼𝗴𝗼𝘂𝘁 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ")
    await sessions_col.delete_one({"_id": user_id})
    
