from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from AuthNex import app
from AuthNex import Database as data
@Client.on_message(filters.command("refferal"))
async def rrefer_someone(_, message):
    user = message.from_user.id
    session = data.sessions_col.find_one({"_id": _id})
    if not session:
        return await message.reply("No login found for ID")
    Link = f"https://t.me/AuthNexBot?start={user}"
    await message.reply(f"**__This is your WARRIOR reffer link\nUSE it to refer someone and get coins__**\n>{Link}")
    pass
