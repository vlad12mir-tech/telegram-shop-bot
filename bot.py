import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 Токен твого бота
TOKEN = '7781139395:AAGUo1NxEFjElW8YuHE9IZLs2U0LL0Seo5w'

# 🔗 ID або username твого каналу (обов'язково!)
CHANNEL_ID = '@AliExpressUkraineDeals'  # або '-1001234567890'

bot = telebot.TeleBot(TOKEN)

# 💱 Курс валют (USD → UAH)
USD_TO_UAH = 39.0

# 📦 Список товарів
products = [
    {
        'title': 'Навушники Bluetooth',
        'url': 'https://s.click.aliexpress.com/e/_oFkv83b',
        'image': 'https://ae01.alicdn.com/kf/S0e222e18c8b949368d6c6e888c382400F.jpg',
        'price_usd': 11.99
    },
    {
        'title': 'Смарт-годинник',
        'url': 'https://s.click.aliexpress.com/e/_oFkv83b',
        'image': 'https://ae01.alicdn.com/kf/S8c912cd6874b4e2bb9b7bc70d70ef5211.jpg',
        'price_usd': 23.50
    }
]

# 👋 /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🇺🇦 Привіт! Тут ти знайдеш топові товари з AliExpress із доставкою в Україну.\n"
        "Натисни /products, щоб переглянути 🔥"
    )

# 🛍️ /products
@bot.message_handler(commands=['products'])
def show_products(message):
    for product in products:
        uah_price = round(product['price_usd'] * USD_TO_UAH, 2)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='🛒 Купити на AliExpress', url=product['url']))
        caption = (
            f"🛍️ *{product['title']}*\n"
            f"💵 Ціна: ${product['price_usd']} (~{uah_price} грн)\n"
            f"[Перейти до товару]({product['url']})"
        )
        bot.send_photo(
            chat_id=message.chat.id,
            photo=product['image'],
            caption=caption,
            parse_mode='Markdown',
            reply_markup=markup
        )

# 📣 /post — публікація товарів у канал
@bot.message_handler(commands=['post'])
def post_to_channel(message):
    for product in products:
        uah_price = round(product['price_usd'] * USD_TO_UAH, 2)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='🛒 Купити на AliExpress', url=product['url']))
        caption = (
            f"🔥 *{product['title']}*\n"
            f"💵 ${product['price_usd']} (~{uah_price} грн)\n"
            f"📦 З доставкою в Україну!\n"
            f"[Перейти до товару]({product['url']})"
        )
        bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=product['image'],
            caption=caption,
            parse_mode='Markdown',
            reply_markup=markup
        )
    bot.send_message(message.chat.id, "✅ Товари надіслано до каналу!")

# 🚀 Запуск
print("Бот працює...")
bot.infinity_polling()

    )

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
