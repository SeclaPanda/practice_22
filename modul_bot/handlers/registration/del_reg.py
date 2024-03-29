import sqlite3
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.kb_group import groups_upd
from keyboards.y_n_kb import get_yes_no_kb

router = Router()

conn = sqlite3.connect(r'./modul_bot/database/groups.db') #подключение и указатель БД 
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    confirm = State()

@router.message(Command('del_reg'))#функция удаления зарегестрированного студента
async def del_reg(message: Message, state: FSMContext):
    await message.answer('Вы уверены что хотите удалить себя из базы данных? Предупреждаю, что после этого вы можете пропустить важное сообщение от преподавателя!', reply_markup=get_yes_no_kb())
    await state.set_state(UserState.confirm)

@router.message(UserState.confirm, Text(text = "да", ignore_case = True))
async def yes(message: Message):    
    groups = groups_upd()
    group = None
    for i in groups:
        cur.execute(f'SELECT userid FROM "{i}" where userid = {str(message.from_user.id)}')
        if cur.fetchone() is not None:
            group = i
    if group is not None:
        cur.execute(f'DELETE FROM "{group}" where userid = ?', (str(message.from_user.id),))
        conn.commit()
        await message.answer(f'Жаль, конечно, но что поделать! Теперь запись о тебе удалена из группы {group}:( Возвращайся!')
    else: 
        await message.answer('Эй! Ты ведь еще даже не зарегестрирован! Как же тебя удалить из базы зарегестрированных студентов?')

@router.message(UserState.confirm, Text(text = "нет", ignore_case=True))
async def no(message: Message): 
    await message.answer('Вот и славно) Рад, что ты остаешься с нами!')