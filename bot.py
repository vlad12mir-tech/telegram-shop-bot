import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
EPN_TOKEN = os.getenv("EPN_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Надішли мені ключове слово, і я знайду товари на AliExpress із партнерськими посиланнями 😉")

def search_aliexpress(query):
    url = "https://api.epn.bz/json/epn-api/search"
    params = {
        "token": EPN_TOKEN,
        "query": query,
        "lang": "uk",
        "limit": 3,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        results = []
        for item in items:
            title = item.get("title")
            link = item.get("epn_link") or item.get("url")
            price = item.get("price") or "Ціна невідома"
            results.append(f"{title}\nЦіна: {price}\n{link}")
        return results if results else ["Нічого не знайдено 😕"]
    else:
        return ["Помилка при запиті до EPN API 😓"]

def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    update.message.reply_text("Шукаю товари...")
    results = search_aliexpress(query)
    for result in results:
        update.message.reply_text(result)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("✅ Бот запущено!")
    updater.idle()

if __name__ == "__main__":
    main()

