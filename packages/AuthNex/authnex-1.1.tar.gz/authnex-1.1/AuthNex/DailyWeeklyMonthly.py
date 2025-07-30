# rewards.py

from pyrogram import Client, filters
from pyrogram.types import Message
from AuthNex import app
from AuthNex.Database import user_col, sessions_col
from datetime import datetime, timedelta

REWARDS = {
    "daily": {"yen": 50000, "xp": 1000, "valor": 10, "drop": "🔑"},
    "weekly": {"yen": 150000, "xp": 4000, "valor": 50, "drop": "🧿"},
    "monthly": {"yen": 500000, "xp": 10000, "valor": 200, "drop": "👑"},
}

LAST_CLAIM_FIELDS = {
    "daily": "last_daily",
    "weekly": "last_weekly",
    "monthly": "last_monthly"
}

@app.on_message(filters.command(["daily", "weekly", "monthly"]), group=31)
async def claim_rewards(_, m: Message):
    reward_type = m.command[0].lower()
    user_id = m.from_user.id

    session = await sessions_col.find_one({"_id": user_id})
    if not session:
        return await m.reply("❌ You are not logged in. Use `/login` first.")

    user = await user_col.find_one({"Mail": session['mail']})
    now = datetime.utcnow()

    last_claim_field = LAST_CLAIM_FIELDS[reward_type]
    last_claim_time = user.get(last_claim_field)

    cooldown = {
        "daily": timedelta(days=1),
        "weekly": timedelta(weeks=1),
        "monthly": timedelta(days=30)
    }[reward_type]

    if last_claim_time and now - last_claim_time < cooldown:
        remaining = cooldown - (now - last_claim_time)
        return await m.reply(f"⏳ You already claimed **{reward_type}** rewards.\nCome back in `{str(remaining).split('.')[0]}`.")

    reward = REWARDS[reward_type]

    await user_col.update_one(
        {"Mail": session["mail"]},
        {
            "$inc": {
                "yen": reward["yen"],
                "xp": reward["xp"],
                "valor": reward["valor"]
            },
            "$set": {
                last_claim_field: now
            }
        }
    )

    msg = f"""
╭── ❰ 𝗥 𝗘 𝗪 𝗔 𝗥 𝗗 ❱ ──╮
│ 💴  𝗬𝗘𝗡       ┃ +{reward['yen']}
│ ✨️  𝗫𝗣        ┃ +{reward['xp']}
│ 🎁  𝗗𝗥𝗢𝗣𝗦     ┃ {reward['drop']}
│ 🏰 𝗞𝗜𝗡𝗚𝗗𝗢𝗠  ┃ +{reward['valor']} 𝘃𝗮𝗹𝗼𝗿
╰────────────────────╯
✅ Claimed your **{reward_type.upper()}** reward!
"""
    await m.reply(msg)
