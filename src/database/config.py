import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Параметры подключения к БД
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Формируем URL подключения
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Loaded DATABASE_URL: {DATABASE_URL}")