from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
import secrets
import asyncio

from AuthNex import app
from AuthNex.Database import user_col, sessions_col, tokens_col

pending_token_users = {}

async def generate_authnex_token(length=50):
    return secrets.token_hex(length // 2)

@Client.on_message(filters.command("generatetoken") & filters.private, group=14)
async def token_command_handler(_, message: Message):
    user_id = message.from_user.id

    if message.chat.type != ChatType.PRIVATE:
        return await message.reply("❌ Use this command in **private chat only.**")

    session = await sessions_col.find_one({"_id": user_id})
    if not session:
        return await message.reply("❌ You must be logged in to generate a token.")

    mail = session.get("mail")
    user = await user_col.find_one({"Mail": mail})
    if not user:
        return await message.reply("⚠️ User record not found.")

    existing_token = await tokens_col.find_one({"_id": user_id})
    if existing_token:
        return await message.reply("✅ You already have a token.\nUse `/revoketoken` to regenerate.")

    pending_token_users[user_id] = {
        "mail": mail,
        "password": user["Password"]
    }
    await message.reply("🔐 Send your **password** to confirm token generation.\n\n⚠️ Type `cancel` to abort.")

@Client.on_message(filters.private & filters.text, group=13)
async def password_listener(_, message: Message):
    user_id = message.from_user.id
    if user_id not in pending_token_users:
        return

    input_text = message.text.strip()
    if input_text.lower() == "cancel":
        del pending_token_users[user_id]
        return await message.reply("❌ Token generation cancelled.")

    expected_pass = pending_token_users[user_id]["password"]
    mail = pending_token_users[user_id]["mail"]

    if input_text != expected_pass:
        del pending_token_users[user_id]
        return await message.reply("❌ Incorrect password. Try again.")

    # Generate unique token
    while True:
        token = await generate_authnex_token()
        if not await tokens_col.find_one({"token": token}):
            break

    await tokens_col.insert_one({
        "_id": user_id,
        "mail": mail,
        "token": token
    })

    del pending_token_users[user_id]

    await message.reply(f"✅ **Your AuthNex Token:**\n\n`{token}`\nUse this to authenticate with **AuthNex-based bots/libraries.**")
