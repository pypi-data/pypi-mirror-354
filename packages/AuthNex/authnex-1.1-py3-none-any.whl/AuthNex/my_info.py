from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from AuthNex import app
from AuthNex.Database import user_col, sessions_col

@Client.on_message(filters.command('myinfo') & (filters.private), group=16)
async def accounts_handler(client: Client, m: Message):
    _id = m.from_user.id

    # Check if session exists
    session = await sessions_col.find_one({"_id": _id})
    if not session:
        return await m.reply("❌ You are not logged in. Use `/login` first.")

    # Fetch user data
    user = await user_col.find_one({"Mail": session.get('mail')})
    if not user:
        return await m.reply("❌ User data not found.")

    # Fetch profile picture
    photos = await client.get_profile_photos(_id, limit=1)
    if not photos:
        return await m.reply("❌ No profile picture found.")

    # Download profile pic
    pic = await client.download_media(photos[0].file_id)

    # Reply with info and profile pic
    await m.reply_photo(
        photo=pic,
        caption=f"""**🔐 AuthNex Profile**

👤 **Name:** `{user.get('Name')}`
🆔 **User ID:** `{_id}`
📧 **Email:** `{user.get('Mail')}`
🔰 **AuthCoins:** {user.get('AuthCoins')}
🧪 **Password:** {user.get('Password')}
🔑 **Token:** `{user.get('token', 'Not Generated')}`
""",
        parse_mode=ParseMode.MARKDOWN
    )
