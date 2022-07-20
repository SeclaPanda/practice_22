import logging
from asyncio import sleep
from pyexpat.errors import messages
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked


# Объект бота
bot = Bot(token='5432818658:AAHNCv2cCmy9f2L5aoxgJInct_kP0fZrvvk')
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Хэндлер на команду /test1
@dp.message_handler(commands='test1')
async def cmd_test1(message: types.Message):
    await message.reply ('Test 1')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply ('Здравствуйте!')
    sleep(2)
    await message.answer ('Вас приветствует бот-помощник преподавателя ИУЦТ')
    sleep(2)
    await message.answer ('Мой функционал пока ограничен, но мой создатель очень старается!')
    sleep(2)
    await bot.send_message(message.from_user.id, 'Для начала предлагаем вам зарегестрироваться!')
    sleep(2)
    await message.answer ('Если вы готовы сделать это сейчас введите: рег или регистрация или /reg')


@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.reply ('RN I only can /start /help /reg')

@dp.message_handler(content_types='text')
async def text(message):
    if (message.text == 'рег') or (message.text == 'регистрация') or (message.text == '/reg'):
        await reg(message)   
    else:
        await message.reply ('Can\'t understand you. Send /help')    

@dp.message_handler(commands='reg')
async def reg(message: types.Message):
    #dp.register_message_handler(message, get_name)
    await message.reply ('Send your name')
    '''await''' 
    get_name(message)


async def get_name(message: types.Message): #получаем имя
    global name
    name = message.text
    #dp.register_message_handler(message, get_surname)
    await message.reply ('Send your surname')
    #await 
    get_surname(message)

async def get_surname(message: types.Message):
    global surname
    surname = message.text
    await message.reply (f'You are {name} {surname}')
    await message.reply ('Glad to know you!')

@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True

if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
