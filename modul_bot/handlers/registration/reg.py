import sqlite3
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.kb_group import make_kboard, groups_upd
from handlers.registration import n_group, del_reg

router = Router()
router.include_routers(del_reg.router, n_group.router)#, wrt.router)

conn = sqlite3.connect(r'./modul_bot/database/groups.db') #подключение и указатель БД 
cur = conn.cursor()

async def hascyr(s): #проверка, что буквы русского алфавита
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(s.lower()) != set() 

class UserState(StatesGroup): #передача переменных 
    reg = State()
    name = State()

#регистрационная панель студентов в группы
@router.message(Command('reg'))
async def reg(message: Message, state: FSMContext): 
    await state.set_state(UserState.reg)
    await message.answer("Нажми на кнопку и выбери группу ", reply_markup=make_kboard())
    
@router.message(UserState.reg, F.text.casefold() != 'новая группа')
#функция регистрации студентов
async def wrt(message: Message, state: FSMContext):
    groups = groups_upd()
    registred = False
    for i in groups:
        cur.execute(f'SELECT userid FROM "{i}" where userid = ?', (str(message.from_user.id),))
        if cur.fetchone() is not None:
            registred = True
            group = i
    if registred == False:
        await state.update_data(reg = message.text)    
        await state.set_state(UserState.name)
        await message.answer('Отлично! Представься пожалуйста - ФИО:')
    else:
        await message.answer(f'Хэй! Кажется ты уже зарегестрирован в группе - {group}) Не пытайся меня обмануть, пожалуйста!')
        await state.clear()

@router.message(UserState.name)
async def registration(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    name = data['name'] 
    group = data['reg']
    flag = False
    tmp = [''.join(i.capitalize()) for i in name.split()]
    name = ' '.join(tmp)
    print(list(name))
    for j in list(name):
        if j == ' ':
            continue
        if await hascyr(j) != True:
            flag = False
            break
        else:
            flag = True
        print(flag)
    if flag == True:
    #if hascyr(name) == True:
        query = f'INSERT INTO "{group}" VALUES (\'{str(message.from_user.id)}\', \'{message.from_user.username}\', \'{name}\');'
        cur.execute(query)
        conn.commit()
        await state.clear()
        await message.answer('Супер! Теперь ты зарегистрирован(-а). Дальше, просто ожидай сообщений от преподавателей!')
    else:
        await state.set_state(UserState.name)
        await message.answer('Видимо вы ввели ФИО содержащие символы латиницы! Пожалуйста, введите ФИО на кирилице!')