import contextlib, sqlite3, re
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text
from keyboards.gr_check_kb import get_kb, make_kboard

router = Router()
conn = sqlite3.connect(r'./groups/groups.db') #подключение и указатель БД 
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    num_group = State()

@router.message(Command('gr_check')) #функция проверки количества студентов в группе
async def gr_check(message: Message, state: FSMContext):
    await message.answer('Выберите группу которую хотите проверить на количество зарегестрированных студентов', reply_markup=make_kboard())
    await state.set_state(UserState.num_group)
    
@router.message(UserState.num_group)# вывод кол-ва студентов в группе
async def gr(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text = "/work")
    btn2 = KeyboardButton(text = "/help")
    markup.add(btn1, btn2)
    cur.execute(f"select count(*) from {message.text}")
    row_count = cur.fetchone()
    await message.answer(f'Количество студентов в группе {message.text} равно {row_count[0]}')
    await message.answer(f'Моежете вернуться к отправке сообщений студентам с помощью команды /work \nИли же прочитать справку через команду /help', reply_markup=get_kb())