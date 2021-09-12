from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Initialising Bot
updater = Updater(
    token="1867473854:AAEpabnZ1l7HOK0Oth7tQHRpIjAW8WiXPTk", use_context=True
)
dispatcher = updater.dispatcher

# Initialising Debug Logs
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Bot Functions
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Generating 11 Minor! Please input details as requested.",
    )


def echo(update, context):
    usertext = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Bot Handles
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# Running
updater.start_polling()