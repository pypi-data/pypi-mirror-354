# shop_command.py

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from AuthNex import app
from AuthNex.Database import sessions_col, user_col
from AuthNex.items import SHOP_ITEMS


@Client.on_message(filters.command("shop"), group=29)
async def view_shop(_, m: Message):
    session = await sessions_col.find_one({"_id": m.from_user.id})
    if not session:
        return await m.reply("❌ You are not logged in via AuthNex.")

    buttons = []
    for code, item in SHOP_ITEMS.items():
        buttons.append([InlineKeyboardButton(f"Buy {item['name']} - {item['price']}💰", callback_data=f"buy_{code}")])

    await m.reply("🛒 **Welcome to AuthNex Shop!**\n\n" + "\n".join(
        [f"• `{item['name']}` — {item['price']} Coins\n  _{item['description']}_" for item in SHOP_ITEMS.values()]
    ), reply_markup=InlineKeyboardMarkup(buttons))
  # shop_callback.py


@Client.on_callback_query(filters.regex(r"^buy_"), group=30)
async def buy_item(_, cq: CallbackQuery):
    user_id = cq.from_user.id
    session = await sessions_col.find_one({"_id": user_id})
    if not session:
        return await cq.answer("❌ Login required.", show_alert=True)

    user = await user_col.find_one({"Mail": session['mail']})
    item_code = cq.data.split("_", 1)[1]
    item = SHOP_ITEMS.get(item_code)

    if not item:
        return await cq.answer("❌ Invalid item.", show_alert=True)

    user_coins = user.get("AuthCoins", 0)
    if user_coins < item['price']:
        return await cq.answer("❌ Not enough AuthCoins.", show_alert=True)

    await user_col.update_one({"_id": user["_id"]}, {
        "$inc": {"AuthCoins": -item['price'], item_code: 1}
    })
    await cq.answer(f"✅ Bought {item['name']}!", show_alert=True)
    await cq.message.edit_text(f"🛒 You bought **{item['name']}** for {item['price']} Coins!\nBalance: {user_coins - item['price']}💰")
