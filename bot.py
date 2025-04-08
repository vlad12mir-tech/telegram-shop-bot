from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import logging
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

products = [
    {"name": "Гаджет 1", "price": "500 грн"},
    {"name": "Гаджет 2", "price": "750 грн"},
]

@dp.message_handler(commands=["start", "help"])
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    for i, product in enumerate(products):
        keyboard.add(InlineKeyboardButton(
            text=f"{product['name']} – {product['price']}",
            callback_data=f"buy_{i}"
        ))
    await message.answer("Оберіть товар:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("buy_"))
async def process_callback(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split("_")[1])
    product = products[index]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f"Ви обрали: {product['name']} за {product['price']}
Незабаром з вами зв'яжеться оператор."
    )

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
