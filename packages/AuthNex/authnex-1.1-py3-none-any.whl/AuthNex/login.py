from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import datetime
from AuthNex import app
from AuthNex.Database import user_col, sessions_col
from AuthNex.Modules.auth import authentication_code
login_state = {}
otp_pending = {}

@Client.on_message(filters.command("login") & filters.private, group=8)
async def start_login(_, message: Message):
    user_id = message.from_user.id
    if await sessions_col.find_one({"_id": user_id}):
        return await message.reply("You already have a account ")
    login_state[user_id] = {"step": "mail"}
    await message.reply("📧 Please enter your **mail** to login:")

@app.on_message(filters.text & filters.private)
async def handle_login_input(_, message: Message):
    user_id = message.from_user.id
    if user_id not in login_state:
        return
    state = login_state[user_id]
    text = message.text.strip()

    # STEP 1: Mail Input
    if state["step"] == "mail":
        state["mail"] = text
        state["step"] = "password"
        await message.reply("🔐 Enter your **password**:")

    # STEP 2: Password Input
    elif state["step"] == "password":
        mail = state["mail"]
        password = text

        user = await user_col.find_one({"Mail": mail, "Password": password})
        if not user:
            await message.reply("❌ Invalid mail or password.")
            del login_state[user_id]
            return

        existing_session = await sessions_col.find_one({"mail": mail})
        
        # CASE 1: No session — direct login
        if not existing_session:
            await sessions_col.insert_one({
                "_id": user_id,
                "mail": mail,
                "login_time": datetime.datetime.utcnow()
            })
            await message.reply(f"✅ Logged in successfully as `{user.get('Name')}`.")
            del login_state[user_id]
            return

        # CASE 2: Someone already logged in → send OTP to current owner
        code = await authentication_code(mail, existing_session["_id"])
        otp_pending[user_id] = {
            "otp": code,
            "mail": mail,
            "name": user.get("Name"),
            "old_user_id": existing_session["_id"]
        }

        state["step"] = "otp"
        await message.reply("📨 Someone is already logged in with this mail.\nEnter the **OTP** sent to the registered Telegram account to continue.")

        # Send code to old user
        try:
            await app.send_message(
                existing_session["_id"],
                f"⚠️ A login attempt was made for your account by `{message.from_user.first_name}`.\nHere is your OTP: `{code}`"
            )
        except:
            await message.reply("❌ Failed to send OTP to the original user.")
            del login_state[user_id]
            return

    # STEP 3: OTP Verification
    elif state["step"] == "otp":
        user_otp = text
        otp_info = otp_pending.get(user_id)

        if not otp_info or user_otp != otp_info["otp"]:
            await message.reply("❌ Incorrect OTP. Login denied.")
            del login_state[user_id]
            otp_pending.pop(user_id, None)
            return

        # Add new login (do not remove old)
        await sessions_col.insert_one({
            "_id": user_id,
            "mail": otp_info["mail"],
            "login_time": datetime.datetime.utcnow()
        })

        await message.reply(f"✅ OTP verified! Logged in as `{otp_info['name']}`.")
        del login_state[user_id]
        otp_pending.pop(user_id, None)

        # Notify old user
        try:
            await app.send_message(
                otp_info["old_user_id"],
                f"⚠️ New login detected for your account by `{message.from_user.first_name}`.\nDo you want to take action?",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ It's safe", callback_data="safe_login")],
                    [InlineKeyboardButton("❌ Terminate", callback_data=f"terminate:{user_id}")]
                ])
            )
        except:
            pass
from pyrogram.types import CallbackQuery

@Client.on_callback_query(filters.regex("^(safe_login|terminate:)"), group=17)
async def login_action(_, query: CallbackQuery):
    data = query.data
    if data == "safe_login":
        await query.answer("✅ Marked as safe.", show_alert=True)
        await query.edit_message_text("✅ You accepted the new login.")
    elif data.startswith("terminate:"):
        target_id = int(data.split(":")[1])
        await sessions_col.delete_one({"_id": target_id})
        await app.send_message(target_id, "❌ Your session was terminated by the account owner.")
        await query.answer("Terminated the new login session.", show_alert=True)
        await query.edit_message_text("❌ Login terminated.")
