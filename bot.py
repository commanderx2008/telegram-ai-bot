import os
import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv("bot.env")
API_TOKEN = os.getenv("API_TOKEN")
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

if not API_TOKEN:
    raise ValueError("API_TOKEN не найден. Проверьте .env")
if not DEEPINFRA_API_KEY:
    raise ValueError("DEEPINFRA_API_KEY не найден. Проверьте .env")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавиатура с добавленной кнопкой "Старт"
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Решить задачу"), KeyboardButton(text="ℹ️ О боте")],
        [KeyboardButton(text="📞 Связь с тех. поддержкой")],
        [KeyboardButton(text="🚀 Старт")]
    ], resize_keyboard=True
)


# Функция для решения задач через DeepInfra
async def solve_task_with_ai(task: str) -> str:
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
    data = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "messages": [{"role": "user", "content": task}],
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return "Ошибка при решении задачи. Попробуйте позже."


# Команда /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("👋 Привет! Я помогу решить твои задачи. Отправь текст или нажми кнопку!", reply_markup=kb)


# Кнопка "О боте"
@dp.message(lambda message: message.text == "ℹ️ О боте")
async def about_handler(message: types.Message):
    await message.answer("🤖 Я бот, который решает задачи с помощью ИИ! Напиши задачу, и я помогу!")


# Кнопка "Решить задачу"
@dp.message(lambda message: message.text == "📚 Решить задачу")
async def task_request_handler(message: types.Message):
    await message.answer("✍️ Отправь задачу, и я попробую её решить!")


# Кнопка "Связь с тех. поддержкой"
@dp.message(lambda message: message.text == "📞 Связь с тех. поддержкой")
async def support_handler(message: types.Message):
    support_info = """
    📧 Для связи с технической поддержкой пишите на email:
    xcommander67@gmail.com

    📱 Или напишите в наш Telegram канал: @support_channel
    """
    await message.answer(support_info)


# Кнопка "Старт"
@dp.message(lambda message: message.text == "🚀 Старт")
async def start_button_handler(message: types.Message):
    await message.answer("Вы нажали на кнопку Старт! Отправьте задачу, чтобы я помог вам её решить.", reply_markup=kb)


# Обработчик текстовых сообщений (решение задач)
@dp.message()
async def solve_task_handler(message: types.Message):
    task = message.text.strip()
    if not task:
        await message.answer("❌ Пожалуйста, отправь текст задачи!")
        return

    await message.answer("⏳ Думаю...")
    solution = await solve_task_with_ai(task)
    await message.answer(f"✅ Решение:\n{solution}")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
