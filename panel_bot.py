import telebot
from tinydb import TinyDB, Query

# ✅ Bot Token aur Admin ID
BOT2_TOKEN = "8405398342:AAHYG2N0CJu7Bm_3C9B9C3vRpqqM40FNdU0"
ADMIN_ID = 5859078267  # Tera Telegram ID

# ✅ Payment Details
PAYMENT_UPI = "8263838399@ybl"
PAYMENT_NAME = "Gaurav Khairnar"

# ✅ Initialize Bot & DB
bot = telebot.TeleBot(BOT2_TOKEN)
db = TinyDB("db.json")
stock_status = {"available": True}

# =========================
# ✅ Start Command
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, f"📊 Panel Bot Ready!\nCommands:\n/stock_on\n/stock_off\n/orders\n\n💰 Payment Info:\nUPI: {PAYMENT_UPI}\nName: {PAYMENT_NAME}")
    else:
        bot.reply_to(message, "❌ Access Denied (Admin Only)")

# =========================
# ✅ Stock Control
# =========================
@bot.message_handler(commands=["stock_on"])
def stock_on(message):
    if message.chat.id == ADMIN_ID:
        stock_status["available"] = True
        bot.send_message(ADMIN_ID, "✅ Stock is now AVAILABLE")

@bot.message_handler(commands=["stock_off"])
def stock_off(message):
    if message.chat.id == ADMIN_ID:
        stock_status["available"] = False
        bot.send_message(ADMIN_ID, "❌ Stock is now UNAVAILABLE")

# =========================
# ✅ New Order Add (called by BOT 1)
# =========================
def add_order(user_id, username, package, amount):
    order = {
        "user_id": user_id,
        "instagram": username,
        "followers": package,
        "amount": amount,
        "status": "pending"
    }
    db.insert(order)
    bot.send_message(ADMIN_ID, f"🆕 New Order!\n👤 TG ID: {user_id}\n📸 IG: @{username}\n👥 Followers: {package}\n💰 ₹{amount}\n📦 Status: Pending")

# =========================
# ✅ Show Orders
# =========================
@bot.message_handler(commands=["orders"])
def show_orders(message):
    if message.chat.id == ADMIN_ID:
        orders = db.all()
        if not orders:
            bot.send_message(ADMIN_ID, "📭 No orders yet")
            return
        text = "📋 Orders:\n"
        for o in orders:
            text += f"- @{o['instagram']} | {o['followers']} | ₹{o['amount']} | {o['status']}\n"
        bot.send_message(ADMIN_ID, text)

# =========================
# ✅ Run Bot
# =========================
print("✅ Panel Bot Running...")
bot.polling()