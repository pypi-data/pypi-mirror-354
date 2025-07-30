<h1 align="center">🚀 AUTHNEX - Telegram Auth Engine + Gaming Bot Suite</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Power-AuthNex-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Pyrogram-v2-blue.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/Python-3.10+-green?style=flat-square" />
  <img src="https://img.shields.io/badge/MongoDB-Atlas-informational?style=flat-square" />
</p>

<p align="center">
  <b>Modular Auth + Coin System + Game League + Roleplay Engine</b><br>
  Built for advanced Telegram bots without requiring user clients.
</p>

---

## 🧠 What is AuthNex?

**AuthNex** is a multi-functional, advanced modular Telegram bot system that provides:
- 🔐 User Authentication (via Mail/Password + OTP)
- 🪙 Coin + XP + Valor System
- 🎮 Adventure Quests, Daily Rewards, Merchants
- ⚔️ League-based Tournament System
- 🛒 In-bot AuthNex Shop
- 📦 Admin Tools: Broadcasts, Ban, Tournament Control
- 🎁 Drops, Roleplay Items, Rewards, and More!

---

## 📦 Features at a Glance

| Feature               | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| 🎮 AuthNex Game Engine| Adventure, currency rewards (¥, €, $), random merchant encounters  |
| 🏦 AuthCoin System    | Currency + item tracking (yen, xp, valor, drops)                  |
| 🔑 Login Engine       | Secure auth using OTP + password (session-based)                  |
| 🏰 Tournaments        | League + Reward system with top-3 prize coins                     |
| 🛍️ AuthNex Shop       | Purchase in-game items, permits, boosts                           |
| 💬 Broadcast System   | Owner sends message to all users                                   |
| ⏳ Reward Cooldowns    | Daily / Weekly / Monthly claim with cooldown checks               |
| ⚠️ Secure SUDO system | SUDO-based commands, admin actions restricted                     |

---

## ⚙️ Setup

```bash
git clone https://github.com/RyomenSukuna53/AuthNex
cd AuthNex

pip install -r requirements.txt
python3 -m bot

> Edit config.py with your MongoDB URI, API_ID, API_HASH, BOT_TOKEN, and SUDO list.




---

🧾 MongoDB Structure

user_col → Stores user Mail, Password, Name, coins, drops

sessions_col → Tracks who is logged in

JoinedPlayers → For tournament participations

shop_col (optional) → If you want custom shop inventory



---

🛠️ Admin Commands

Command	Access	Description

/broadcast	SUDO	Sends message to all users
/startuor	SUDO	Starts a new tournament
/endtournament	SUDO	Ends tournament, rewards top players



---

🔐 User Commands

Command	Description

/create_acc	Start account creation (Mail + Password)
/login	Log in using your credentials
/daily	Claim daily reward
/weekly	Claim weekly reward
/monthly	Claim monthly reward
/adventure	Start a random quest and get money or encounter merchant
/shop	View and purchase AuthNex items
/profile	View your XP, Valor, Drops, Currency
/joinuor	Join an ongoing tournament if eligible



---

🏆 Tournament Logic

Must have 1000 AuthCoins and a TCA (Tournament Permit)

Only SUDO can start and end tournaments

On end:

🥇 1st gets +5000

🥈 2nd gets +2500

🥉 3rd gets +1000




---

🎁 Rewards Example

╭── ❰ 𝗥 𝗘 𝗪 𝗔 𝗥 𝗗 ❱ ──╮
│ 💴  𝗬𝗘𝗡       ┃ +50000
│ ✨️  𝗫𝗣        ┃ +1000
│ 🎁  𝗗𝗥𝗢𝗣𝗦     ┃ 🔑
│ 🏰 𝗞𝗜𝗡𝗚𝗗𝗢𝗠  ┃ +10 𝘃𝗮𝗹𝗼𝗿
╰────────────────────╯
✅ Claimed your **DAILY** reward!


---

📈 Leaderboards & Stats

Coming soon in /leaderboard

Tracks top 10 players based on XP or Valor



---

🧪 Shop Items (JSON Format)

SHOP_ITEMS = {
    "permit": {"price": 2000, "emoji": "📜", "desc": "Tournament Access"},
    "xp_boost": {"price": 500, "emoji": "⚡", "desc": "+2x XP for 24hr"},
    "mystery_box": {"price": 3000, "emoji": "🎁", "desc": "Random Reward"}
}


---

👻 Hidden Mechanics

merchant appears only with 0.111% rarity in adventures

Rare drops grant:

TCA (tournament access)

+€10,000 or 💵10,000 or 💴50,000 depending on luck


Dungeons may be added soon...



---

📢 Broadcast Example

@app.on_message(filters.command(["broadcast", "bcast"]) & filters.user(SUDO))
async def broadcast(_, m):
    users = await user_col.find_many()
    for user in users:
        try:
            await app.send_message(user["_id"], m.text.split(None, 1)[1])
        except:
            continue
    await m.reply("✅ Broadcast complete.")


---

📣 Upcoming Features

🎭 Roleplay mode

🏹 Dungeon crawling

🪙 Trading economy

🗝️ More rare drops

📤 Referral system

🌍 Leaderboard site (exported data)



---

❤️ Special Thanks

> 🧙 Built with love by @RyomenSukuna53
Contributions and issues welcome!




---

License

This project is under the MIT License. Use it, extend it, and improve it.


---
```
<div align="center">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&pause=1000&center=true&vCenter=true&width=435&lines=Welcome+to+AuthNex+World!;Prepare+for+Battle!;Level+Up+Everyday!">
</div>

---
