# adventure.py

from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
from AuthNex import app
from AuthNex.Database import user_col, sessions_col
import random

CURRENCIES = [
    {"name": "YEN", "amount": lambda: random.randint(1000, 30000), "emoji": "💴"},
    {"name": "DOLLAR", "amount": lambda: random.randint(10, 100), "emoji": "💵"},
    {"name": "EURO", "amount": lambda: random.randint(20, 200), "emoji": "💶"},
]

@Client.on_message(filters.command("adventure"), group=32)
async def go_on_adventure(_, m: Message):
    user_id = m.from_user.id
    session = await sessions_col.find_one({"_id": user_id})
    if not session:
        return await m.reply("❌ Please login with an AuthNex account first.")

    user = await user_col.find_one({"Mail": session["mail"]})
    
    # 12-hour cooldown
    last_adventure = user.get("last_adventure")
    now = datetime.utcnow()
    if last_adventure and (now - last_adventure) < timedelta(hours=12):
        rem = timedelta(hours=12) - (now - last_adventure)
        return await m.reply(f"⏳ Adventure cooldown! Come back in `{str(rem).split('.')[0]}`")

    reward_chance = random.random()

    if reward_chance <= 0.00111:
        # 🎴 Merchant Found
        await user_col.update_one({"Mail": session.get("mail")}, {"$set": {"last_adventure": now}})
        return await m.reply("""
🧔‍♂️ You stumbled upon a **mysterious merchant**...  
He whispers: _"Shhh... I've got secret AuthNex accounts for sale."_  
But he vanished before you could respond!  
**Rarity:** `0.111%` 🃏
""")

    elif reward_chance <= 0.75:
        # 🎉 Got currency
        reward = random.choice(CURRENCIES)
        amount = reward["amount"]()

        await user_col.update_one({"Mail": session.get("mail")}, {
            "$inc": {reward["name"].lower(): amount},
            "$set": {"last_adventure": now}
        })

        return await m.reply(f"""
🧭 **Adventure Complete!**
You found {reward['emoji']} `{amount}` {reward['name']} while exploring the AuthNex Kingdom!
""")

    else:
        # 💀 Found Nothing
        await user_col.update_one({"Mail": session.get("mail")}, {"$set": {"last_adventure": now}})
        return await m.reply("""
🌫️ You wandered through empty lands...  
Nothing was found, but the experience was priceless.  
Try again later!
""")
