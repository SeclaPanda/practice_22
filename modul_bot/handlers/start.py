import contextlib, sqlite3, re
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text

router = Router()

#"стартовая" панель бота
@router.message(Command('start'))
async def start(message: Message):
    with open ('./annotation/start.txt', encoding="utf-8") as s:
        content = s.read()
    await message.reply(content)
    await message.answer('Если вы студент вам необходимо только зарегистрироваться - /reg')
    #f = './id.txt'
    #with open(f, "a") as myfile:
    #    your_variable = (f'{str(message.from_user.id)} - {str(message.from_user.username)}'+ '\n')
    #    myfile.write(your_variable)
    kb = [
        [
            KeyboardButton(text = "/work"),
            KeyboardButton(text = "/help"),
            KeyboardButton(text = "/reg")
        ],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard = True,
        input_field_placeholder="Выберите следующий пункт",
        one_time_keyboard = True
    )
    await message.answer('Для начала работы от лица преподавателя и выбора группы напишите или нажите - /work', reply_markup=markup)