from pyrogram import Client, filters
from pyrogram.types import Message
from AuthNex import app
from AuthNex.Database import user_col, sessions_col

@Client.on_message(filters.command("pay") & filters.private, group=25)
async def pay_command(_, message: Message):
    user = message.from_user
    user_id = user.id

    # Check session
    session = await sessions_col.find_one({"_id": user_id})
    if not session:
        return await message.reply("❌ You are not logged in. Use `/login` first.")

    # Check if command has correct format
    args = message.text.split()
    if len(args) != 3:
        return await message.reply("🪙 Usage: `/pay <@username or user_id> <amount>`")

    target = args[1].strip().replace("@", "")
    try:
        amount = int(args[2])
    except ValueError:
        return await message.reply("❌ Amount must be a valid number.")

    if amount <= 0:
        return await message.reply("❌ Amount must be greater than 0.")

    sender = await user_col.find_one({"_id": user_id})
    if not sender:
        return await message.reply("❌ User not found in AuthNex DB.")

    if sender.get("AuthCoins", 0) < amount:
        return await message.reply("💸 You don’t have enough AuthCoins to complete this transaction.")

    # Find recipient by username or ID
    receiver = await user_col.find_one({"Username": target}) or await user_col.find_one({"_id": int(target)}) if target.isdigit() else None

    if not receiver:
        return await message.reply("❌ Recipient not found in AuthNex system.")

    if receiver["_id"] == sender["_id"]:
        return await message.reply("⚠️ You can't pay yourself.")

    # Update balances
    await user_col.update_one({"_id": sender["_id"]}, {"$inc": {"AuthCoins": -amount}})
    await user_col.update_one({"_id": receiver["_id"]}, {"$inc": {"AuthCoins": amount}})

    await message.reply(f"✅ Payment successful!\nYou sent **{amount} AuthCoins** to `{receiver.get('Name')}`.")

    try:
        await app.send_message(receiver["_id"], f"💸 You received **{amount} AuthCoins** from `{sender.get('Name')}`.")
    except:
        pass  # Ignore if user hasn't started bot
