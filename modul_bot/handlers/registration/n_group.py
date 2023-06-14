import sqlite3
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

conn = sqlite3.connect(r'./modul_bot/database/groups.db') #подключение и указатель БД 
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    group = State()

async def hascyr(s): #проверка, что буквы русского алфавита
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(s.lower()) != set() 

@router.message(F.text.casefold() == 'новая группа')
async def ngr(message: Message, state: FSMContext): #сбор названия новой группы
    await state.set_state(UserState.group)
    await message.answer('введите номер группы в формате: УИС-111')

@router.message(UserState.group) #функция создания новой группы
async def ntxt(message: Message, state: FSMContext):
    await state.update_data(group = message.text)
    data = await state.get_data()
    num_group = data['group'].upper()
    flag = False
    for i in list(num_group):
        if i == '-':
            break
        if await hascyr(i) == True:
            flag = True
        else:
            break
    if flag == True:
        query = (
            'CREATE TABLE IF NOT EXISTS "'
            + num_group
            + '" (userid TEXT PRIMARY KEY, nickname TEXT, full_name TEXT);'
        )
        cur.execute(query)
        conn.commit()
        await state.clear()
        await message.reply('Отлично!  Группа создана! Теперь вернемся через /reg и зарегистрируемся в неё! ЖМИ!')
    else:
        await state.set_state(UserState.group)
        await message.answer('Пожалуйста, введите название группы, согласно заданному формату - УИС-111')