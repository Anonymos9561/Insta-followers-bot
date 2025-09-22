import telebot

# =========================
# ✅ Bot Token & Payment Details
# =========================
BOT1_TOKEN = "8099918258:AAG6v7xaeZ9UqXrn-P0HYl6KvqfrBq8D9k4"
UPI_ID = "8263838399@ybl"
UPI_NAME = "Gaurav Khairnar"

# =========================
# Initialize Bot
# =========================
bot = telebot.TeleBot(BOT1_TOKEN)

# =========================
# Packages
# =========================
packages = {
    "1000": 100,
    "2000": 200,
    "5000": 500
}

user_data = {}

# =========================
# Start Command
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "👋 Welcome!\nUse /order to buy Instagram followers")

# =========================
# Order Command
# =========================
@bot.message_handler(commands=["order"])
def order(message):
    # 💰 Show price list first
    price_list = "💰 Price List:\n"
    for followers, amount in packages.items():
        price_list += f"₹{amount} = {followers} followers\n"
    bot.send_message(message.chat.id, price_list)

    # Ask Instagram username
    bot.send_message(message.chat.id, "✍️ Enter your Instagram username:")
    bot.register_next_step_handler(message, get_username)

def get_username(message):
    user_data[message.chat.id] = {"username": message.text}
    buttons = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for k in packages:
        buttons.add(f"{k}")  # Only numeric value
    bot.send_message(message.chat.id, "📦 Choose package:", reply_markup=buttons)
    bot.register_next_step_handler(message, get_package)

# =========================
# Updated get_package function without QR
# =========================
def get_package(message):
    text = message.text.strip()
    selected_package = None

    # Loop through packages keys
    for key in packages:
        if key in text:
            selected_package = key
            break

    if not selected_package:
        bot.send_message(message.chat.id, "❌ Invalid selection. Try again with /order")
        return

    followers = selected_package
    amount = packages[followers]
    user_data[message.chat.id]["followers"] = int(followers)
    user_data[message.chat.id]["amount"] = amount

    # ✅ Show UPI ID instead of QR
    bot.send_message(
        message.chat.id,
        f"💳 Pay ₹{amount} using UPI\nUPI ID: {UPI_ID}\nName: {UPI_NAME}\n\nAfter payment, wait for confirmation ✅"
    )

    # Send order to Panel Bot
    from panel_bot import add_order
    add_order(
        message.chat.id,
        user_data[message.chat.id]["username"],
        user_data[message.chat.id]["followers"],
        amount
    )

# =========================
# Run Bot
# =========================
print("✅ Public Bot Running...")
bot.polling()