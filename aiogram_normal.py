import logging
import os
import re
from asyncio import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

num = []
# Объект бота
bot = Bot(token='5432818658:AAHNCv2cCmy9f2L5aoxgJInct_kP0fZrvvk')
# Диспетчер для бота
dp = Dispatcher(bot, storage = MemoryStorage())
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

class UserState(StatesGroup):
    group = State()
    text = State()
    group_reg = State()
    n_group = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    with open ('./annotation/start.txt') as s:
        content = s.read()
    await message.reply(content)
    await sleep(1)
    await message.answer('Если вы студент вам необходимо только зарегестрироваться - /reg')
    await sleep(1)
    f = './id.txt' 
    with open(f, "a") as myfile:
        your_variable = str(message.from_user.id) + ' - ' + str(message.from_user.username) + '\n'
        myfile.write(your_variable)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = "/work")
    btn2 = types.KeyboardButton(text = "/help")
    btn3 = types.KeyboardButton(text = "/reg")
    markup.add(btn1, btn2, btn3)
    await message.answer('Для начала работы от лица преподавателя и выбора группы напишите или нажите - /work', reply_markup=markup)

@dp.message_handler(commands=['work'])
async def work(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup()
    directory = './groups' 
    files = os.listdir(directory)
    for i in files:
        i = types.KeyboardButton(f'{i}')
        markup.add(i)
    await message.answer("Нажмите на кнопку и выберите группу ", reply_markup=markup)
    await UserState.group.set()
    
@dp.message_handler(state=UserState.group)
async def snd_msg(message: types.message, state: FSMContext):
    global num
    await state.update_data(group=message.text)
    data = await state.get_data()
    fi = f"./groups/{data['group']}"
    with open (fi) as file_group:
        for inp_str in file_group:
            buf = re.findall(r'\d+', inp_str) 
            num += buf
        for i in num:
            for i in num:
                if (len(i) > 5):
                    continue
                else:
                    num.remove(i)
    await message.answer('Enter text to send: ')
    await UserState.text.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = "/work")
    btn2 = types.KeyboardButton(text = "/help")
    markup.add(btn1, btn2)
    with open ('./annotation/after_work.txt') as a_w:
        content = a_w.read()
    await message.answer(content, reply_markup=markup)

@dp.message_handler(state=UserState.text)
async def snd(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    global num
    for i in num:
        await bot.forward_message(i, message.from_user.id, message.message_id)
    await state.finish()


@dp.message_handler(commands='reg',  content_types='text')
async def reg(message: types.Message, state: FSMContext):
    directory = './groups' 
    files = os.listdir(directory) 
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Новая группа')
    markup.add(btn1)
    for i in files:
        i = types.KeyboardButton(f'{i}')
        markup.add(i)
    await message.answer("Нажми на кнопку и выбери группу ", reply_markup=markup)
    await UserState.group_reg.set()

    @dp.message_handler(state=UserState.group_reg)
    async def check(message: types.message, state: FSMContext):
        await state.update_data(group_reg=message.text)
        data = await state.get_data()
        if (data['group_reg'] == 'Новая группа') or (data['group_reg'] == btn1):
            await ngr(message)
        elif data['group_reg'] not in files:
            await help(message)
            await state.finish()
        else:
            await wrt(data['group_reg'], message)
            await state.finish()


    async def wrt(message, msg):
        fi = f'./groups/{message}'
        registred = False
        with open (fi) as file_group:
            line = str(msg.from_user.id) + ' - ' + str(msg.from_user.username) + '\n'
            for i in file_group:
                if line in i:
                    registred = True
                    await msg.reply('Вы уже зарегестрированы')
            if not registred:
                with open (fi, 'a') as f_g:
                    f_g.write(str(msg.from_user.id) + ' - ' + str(msg.from_user.username) + '\n')
                    await msg.answer('Отлично! Теперь ты зарегестрирован')

    async def ngr(message: types.Message):
        await message.answer('Enter number of group in format: uis_111')
        await UserState.n_group.set()

    @dp.message_handler(state=UserState.n_group)
    async def ntxt(message: types.Message, state: FSMContext):
        await state.update_data(n_group=message.text)
        data = await state.get_data()
        with open (f"./groups/{data['n_group']}.txt", 'x') as f:
            await message.reply('Отлично!  Группа создана! Теперь вернемся через /reg и зарегестрируемся в неё! ЖМИ!')
        await state.finish()

@dp.message_handler(commands='help')
async def help(message: types.Message):
    with open ('./annotation/help.txt') as h:
        content = h.read()
    await message.answer(content)

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