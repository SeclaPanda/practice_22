import contextlib, sqlite3, re
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text
from keyboards.gr_check_kb import get_kb, make_kboard
from keyboards.y_n_kb import get_yes_no_kb

router = Router()
conn = sqlite3.connect(r'./modul_bot/database/groups.db') #подключение и указатель БД 
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    num_group = State()
    stud_list = State()

@router.message(Command('gr_check')) #функция проверки количества студентов в группе
async def gr_check(message: Message, state: FSMContext):
    await state.set_state(UserState.num_group)
    await message.answer('Выберите группу которую хотите проверить на количество зарегестрированных студентов', reply_markup=make_kboard())
    
@router.message(UserState.num_group)# вывод кол-ва студентов в группе
async def gr(message: Message, state: FSMContext):
    await state.update_data(num_group = message.text)
    cur.execute(f'select count(*) from "{message.text}"')
    row_count = cur.fetchone()
    await state.set_state(UserState.stud_list)
    await message.answer(f'Количество студентов в группе {message.text} равно {row_count[0]}')
    await message.answer('Хотите увидеть список зарегистрированных студентов?', reply_markup=get_yes_no_kb())
    

@router.message(UserState.stud_list, F.text.casefold() == 'да')
async def stud_list_y(message: Message, state: FSMContext):
    data = await state.get_data()
    num = data['num_group']
    cur.execute(f'SELECT full_name from "{num}"')
    st_list = (cur.fetchall())
    roster = []
    for i in st_list:
        i = str(i)
        i = re.sub("[(|)|'|,]","",i)
        roster.append(i)
    roster = ', '.join(roster)
    await state.clear()
    await message.answer(f'Список зарегестрированных студентов в группе {num} - {roster}')
    await message.answer(f'Можете вернуться к отправке сообщений студентам с помощью команды /work \nИли же прочитать справку через команду /help', reply_markup=get_kb())

@router.message(UserState.stud_list, F.text.casefold() == 'нет')
async def stud_list_y(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Моежете вернуться к отправке сообщений студентам с помощью команды /work \nИли же прочитать справку через команду /help', reply_markup=get_kb())