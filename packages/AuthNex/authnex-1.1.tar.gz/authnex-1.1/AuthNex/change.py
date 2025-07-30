from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from AuthNex import app
from AuthNex.Database import user_col

async def update_user_field(user_id, field, new_value, user_col):
    result = await user_col.update_one(
        {"_id": user_id},
        {"$set": {field: new_value}}
    )
    return result.modified_count > 0

@Client.on_message(filters.command("changename") & filters.private, group=20)
async def change_name(_, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        return await message.reply("❗ Usage: `/changename YourNewName`", parse_mode=ParseMode.MARKDOWN)

    new_name = args[1]
    success = await update_user_field(message.from_user.id, "Name", new_name, user_col)

    if success:
        await message.reply(f"✅ Name updated to **{new_name}**", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("❌ Failed to update name. Are you registered?")


@Client.on_message(filters.command("changename") & filters.private, group=19)
async def change_name(_, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        return await message.reply("❗ Usage: `/changename YourNewName`", parse_mode=ParseMode.MARKDOWN)

    new_name = args[1]
    success = await update_user_field(message.from_user.id, "Name", new_name, user_col)

    if success:
        await message.reply(f"✅ Name updated to **{new_name}**", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("❌ Failed to update name. Are you registered?")

@Client.on_message(filters.command("changeage") & filters.private, group=18)
async def change_age(_, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        return await message.reply("❗ Usage: `/changeage 18`", parse_mode=ParseMode.MARKDOWN)

    new_age = int(args[1])
    success = await update_user_field(message.from_user.id, "Age", new_age, user_col)

    if success:
        await message.reply(f"✅ Age updated to **{new_age}**")
    else:
        await message.reply("❌ Failed to update age.")




@Client.on_message(filters.command("changeusername") & filters.private, group=17)
async def change_username(_, message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) != 2:
        return await message.reply(
            "❗ **Usage:** `/changeusername your_new_username`",
            parse_mode=ParseMode.MARKDOWN
        )

    new_username = args[1].strip()

    if not new_username.isalnum() or len(new_username) < 3:
        return await message.reply("❌ Username must be at least 3 characters and alphanumeric.")

    user_id = message.from_user.id
    user = await user_col.find_one({"_id": user_id})

    if not user:
        return await message.reply("❌ You are not registered in the system.")

    await user_col.update_one(
        {"_id": user_id},
        {"$set": {"Username": new_username}}
    )

    await message.reply(f"✅ Your username has been updated to **{new_username}**.", parse_mode=ParseMode.MARKDOWN)
