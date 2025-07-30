from AuthNex import app
from AuthNex.Database import user_col, sessions_col
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

@Client.on_message(filters.command('info'), group=6)
async def info(_, m: Message):
    user = m.from_user
    _id = user.id

    # Ensure the command has an argument (e.g. /info email)
    if len(m.command) != 2:
        return await m.reply_text("**𝗜𝗻𝘃𝗮𝗹𝗶𝗱 ❌**\n𝗨𝗦𝗔𝗚𝗘: `/info yourmail@AuthNex.Codes`", parse_mode=ParseMode.MARKDOWN)

    mail = m.command[1]

    if not mail.endswith("@AuthNex.Codes"):
        return await m.reply("**Invalid ❌**\n𝗨𝗦𝗔𝗚𝗘: `/info mail@AuthNex.Codes`", parse_mode=ParseMode.MARKDOWN)

    user_data = await user_col.find_one({"Mail": mail})
    session_data = await sessions_col.find_one({"mail": mail})
    my_session = await sessions_col.find_one({"_id": _id})

    if not user_data:
        return await m.reply("**❌ Invalid Mail**")

    reply = f"𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗 𝚊𝚋𝚘𝚞𝚝 𝙼𝚊𝚒𝚕: `{mail}`\n\n"
    reply += f"**NAME:** `{user_data.get('Name')}`\n"
    reply += f"**AGE:** `{user_data.get('Age')}`\n"
    reply += f"**AUTH-COINS:** `{user_data.get('AuthCoins')}`\n"

    if session_data:
        reply += f"**LOGINED-BY:** [{session_data.get('name')}](tg://user?id={session_data.get('_id')})\n"
        reply += f"**LAST LOGIN:** `{session_data.get('login')}`"

    await m.reply(reply, parse_mode=ParseMode.MARKDOWN)
