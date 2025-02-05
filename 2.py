from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла bot.env
load_dotenv("bot.env")

# Получаем значения переменных
API_TOKEN = os.getenv("API_TOKEN")
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

# Печатаем их для проверки
print(f"API_TOKEN: {API_TOKEN}")
print(f"DEEPINFRA_API_KEY: {DEEPINFRA_API_KEY}")

# Если переменные не найдены, выводим ошибку
if not API_TOKEN or not DEEPINFRA_API_KEY:
    raise ValueError("Одной из переменных окружения не найдено значение. Проверьте bot.env")
