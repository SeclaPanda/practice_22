import asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import start, help, cancel
from handlers.registration import reg
from handlers.t_work import work
from database import clean
from database.reminder import reminder
from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_routers(start.router, help.router, cancel.router, work.router, reg.router)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    #создание расписания на удаление студентов из базы данных в начале первого и второго семестров
    scheduler.add_job(clean.clean, 'cron', day = 1, month = 2, hour = 18, id='job_1')
    scheduler.add_job(clean.clean, 'cron', day = 20, month = 8, hour = 18, id='job_2')
    #создание расписания напоминания студентам зарегестрироваться в группах заново 
    scheduler.add_job(rem, 'cron', day = 1, month = 2, hour = 17, minute = 30, id='job_3')
    scheduler.add_job(rem, 'cron', day = 20, month = 8, hour = 17, minute = 30, id='job_4')

    # Запускаем бота и пропускаем все накопленные входящие
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def rem():
    await reminder(bot)

if __name__ == "__main__":
    asyncio.run(main())