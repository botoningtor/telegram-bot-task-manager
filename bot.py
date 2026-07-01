import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from database import init_db
from handlers import start, tasks

logging.basicConfig(level=logging.INFO)

async def main():
    # Создаем таблицы, если их нет
    await init_db()

    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(tasks.router)

    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
