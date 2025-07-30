from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatType, ParseMode
from AuthNex import app
from AuthNex.Database import JoinedPlayers, sessions_col, user_col
import config
@Client.on_message(filters.command("star_tuor") & filters.user(config.SUDO))
async def TUORNAMENT(_, m: Message):
    _id = m.from_user.id
    session = sessions_col.find_one({"_id": _id})
    if not await session:
        return await m.reply("NOT LOGINED WITH A ACCOUNT PLZ GET AN ACCOUNTS FIRST")
    user = user_col.find_one({"Mail": session.get("mail")})
    if user.get("AuthCoins", 0)<1000:
        return await m.reply("NOT ENOUGH COINS TO CONFIRM")
    if not user.get("TCA", 0)==0:
        return await m.reply("YOU DONT HAVE AUTHENTICATION TOURNAMENT PERTIT PLZ PURCHASE I FIRST OR FOUND IT IN A GROK DOUNGEN")
    await m.reply(">**YOU HAVE TO GIVE YOUR PERMIT AND 1000 COINS TO START", reply_markup=InlineKeyboardMarkup([
        InlineKeyboardButton("PAY", callback_data=f"pay_{_id}")
    ])
                 )
@Client.on_callback_query(filters.regex("^pay"))
async def anything(_, c: CallbackQuery, m: Message):
    pass
