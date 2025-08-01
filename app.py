from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

app = Flask(__name__)
bot = telegram.Bot(token="8103765408:AAFxvE-vmxcbx0AG8vo4_anSDPNAL7J4ncw")

faq = {
    "how to save water": "Fix leaks, use low-flow taps, turn off tap while brushing.",
    "rainwater harvesting": "It is collecting and storing rainwater for reuse.",
    "importance of sanitation": "Sanitation prevents disease and protects water sources.",
}

# Handler function
def handle_message(update, context):
    text = update.message.text.lower()
    for key in faq:
        if key in text:
            update.message.reply_text(faq[key])
            return
    update.message.reply_text("Sorry, I don't know that yet. Try asking about water-saving tips or sanitation.")

@app.route(f"/webhook/{bot.token}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Set up dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

if __name__ == "__main__":
    app.run(debug=True)
