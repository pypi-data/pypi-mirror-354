from pyrogram import Client, filters
from pyrogram.types import Message
from AuthNex import app
from AuthNex.Database import user_col
from config import SUDO

@app.on_message(filters.command(["broadcast", "bcast"]) & filters.private & filters.user(SUDO), group=26)
async def broadcast_by_KURORAIJIN(_, m: Message):
    msg = m.text.split(None, 1)
    if len(msg) < 2:
        return await m.reply("⚠️ Please provide a message to broadcast.\n\nUsage: `/broadcast your message`")

    text = msg[1]
    await m.reply("📢 Broadcast started...")

    success = 0
    failed = 0

    async for user in user_col.find({}):
        try:
            await app.send_message(user["_id"], text)
            success += 1
        except:
            failed += 1

    await m.reply(f"✅ Broadcast finished!\n\n🟢 Success: {success}\n🔴 Failed: {failed}")
