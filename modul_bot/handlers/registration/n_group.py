import sqlite3
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
#from handlers.registration import reg
#from handlers.registration.reg import UserStates

router = Router()

conn = sqlite3.connect(r'modul_bot/database/groups.db') #подключение и указатель БД 
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    group = State()

@router.message(F.text.casefold() == 'новая группа')
async def ngr(message: Message, state: FSMContext): #сбор названия новой группы
    await state.set_state(UserState.group)
    await message.answer('введите номер группы в формате: uis_111')

@router.message(UserState.group) #функция создания новой группы
async def ntxt(message: Message, state: FSMContext):
    await state.update_data(group = message.text)
    data = await state.get_data()
    query = (
        'CREATE TABLE IF NOT EXISTS '
        + data['group']
        + ' (userid TEXT PRIMARY KEY, nickname TEXT, full_name TEXT);'
    )
    cur.execute(query)
    conn.commit()
    await message.reply('Отлично!  Группа создана! Теперь вернемся через /reg и зарегистрируемся в неё! ЖМИ!')
    await state.clear()