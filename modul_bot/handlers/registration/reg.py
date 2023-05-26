import sqlite3
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.kb_group import make_kboard, groups_upd
from handlers.registration import n_group, wrt, del_reg

router = Router()
router.include_routers(del_reg.router, n_group.router) # wrt.router,
conn = sqlite3.connect(r'./groups/groups.db') #подключение и указатель БД 
cur = conn.cursor()
groups = groups_upd()

class UserState(StatesGroup): #передача переменных 
    reg = State()

async def gr_upd():
    return groups_upd()

#регистрационная панель студентов в группы
@router.message(Command('reg'))
async def reg(message: Message, state: FSMContext): 
    #await groups
    await message.answer("Нажми на кнопку и выбери группу ", reply_markup=make_kboard())
    await state.set_state(UserState.reg)

@router.message(UserState.reg, F.text != 'Новая группа')
#функция регистрации студентов
async def wrt(message: Message, state: FSMContext):
    registred = False
    for i in groups:
        cur.execute(f'SELECT userid FROM {i} where userid = ?', (str(message.from_user.id),))
        if cur.fetchone() is not None:
            registred = True
            group = i
    if registred == False:    
        query = f'INSERT INTO {message.text} VALUES (\'{str(message.from_user.id)}\', \'{message.from_user.username}\', \'{message.from_user.full_name}\');'
        cur.execute(query)
        conn.commit()
        await message.answer('Отлично! Теперь ты зарегистрирован')
    else:
        await message.answer(f'Хэй! Кажется ты уже зарегестрирован в группе - {group}) Не пытайся меня обмануть, пожалуйста!')
    await state.clear()
