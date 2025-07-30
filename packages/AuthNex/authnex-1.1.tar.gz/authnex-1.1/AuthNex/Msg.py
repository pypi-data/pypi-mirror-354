#MESSAGE.PY
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType, ParseMode
from AuthNex import app
from AuthNex.Database import sessions_col as session

@Client.on_message(filters.command("msg"), group=24)
async def msg_your_frnd(_, m: Message):
    senderID = m.from_user.id
    if len(m.text) < 3:
        return await m.reply("USAGE: /msg <id> <msg>")
    recieverID = m.text[1]
    sender = await session.find_one({'_id': senderID})
    reciever = await session.find_one({"_id": recieverID})
    if not sender:
        return
    if not reciever:
        return await m.reply("USER NOT FOUND")
    msg = m.text[2:]
    await m.reply("Message sended")
    await Client.send_message(chat_id=recieverID, text=f"Message from {m.from_user.id}\n MSG: {msg}")

MOD_NAME = "MESSAGE.PY"
MOD_USAGE = "/msg {ID} {msg}"
MOD_HELP = "MESSAGE SOMEONE USING HIS ID AND CHAT THEM AND PAY SOME COINS[VERSION[2.0]]"

