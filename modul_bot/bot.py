import asyncio, logging
from aiogram import Bot, Dispatcher
from handlers import start, help
from handlers.registration import reg
from handlers.t_work import work

#https://mastergroosha.github.io/aiogram-3-guide/fsm/

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token="1390660650:AAH6uCX1VOQZSVbuJQsUoPcf-vKkIt_U-Ds")
    dp = Dispatcher()

    dp.include_routers(start.router, work.router, reg.router, help.router)

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())