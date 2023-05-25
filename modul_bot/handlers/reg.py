import contextlib, sqlite3
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from keyboards.kb_group import make_kboard, groups_upd

router = Router()

conn = sqlite3.connect(r'./groups/groups.db') #подключение и указатель БД 
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    group = State()
    text = State()

data = []

#регистрационная панель студентов в группы
@router.message(Command('reg'))
async def reg(message: Message, state: FSMContext):
    await message.answer("Нажми на кнопку и выбери группу ", reply_markup=make_kboard())
    await state.set_state(UserState.group)

    @router.message(UserState.group) #проверяем что выбрали студенты на панели регистрации
    async def check(message: Message):
        groups = groups_upd()
        await state.update_data(group_reg=message.text)
        data = await state.get_data()
        if data['group_reg'] in ['Новая группа']:
            await ngr(message)
            #await state.clear()
        elif data['group_reg'] not in groups:
            #await help(message) if data['group_reg'] == '/cancel' else await help(message)
            await message.answer('Later!')
            await state.clear()
        else:
            await wrt(data['group_reg'], message)
            await state.clear()

    #функция регистрации студентов
    async def wrt(message, msg):
        registred = False
        groups = groups_upd()
        for i in groups:
            cur.execute(f'SELECT userid FROM {i} where userid = ?', (str(msg.from_user.id),))
            if cur.fetchone() is not None:
                registred = True
                group = i
        if registred == False:    
            query = f'INSERT INTO {message} VALUES (\'{str(msg.from_user.id)}\', \'{msg.from_user.username}\');'
            cur.execute(query)
            conn.commit()
            await msg.answer('Отлично! Теперь ты зарегистрирован')
        else:
            await msg.answer(f'Хэй! Кажется ты уже зарегестрирован в группе - {group}) Не пытайся меня обмануть, пожалуйста!')
    
    @router.message(F.text)
    async def ngr(message: Message): #сбор названия новой группы
        await message.answer('введите номер группы в формате: uis_111')
        await state.set_state(UserState.group)
        #await ntxt()

        @router.message(F.text) #функция создания новой группы
        async def ntxt(message: Message):
            await state.update_data(group = message.text)
            data = await state.get_data()
            query = (
                'CREATE TABLE IF NOT EXISTS '
                + data['group']
                + ' (userid TEXT PRIMARY KEY, nickname TEXT);'
            )
            cur.execute(query)
            conn.commit()
            await message.reply('Отлично!  Группа создана! Теперь вернемся через /reg и зарегистрируемся в неё! ЖМИ!')
            await state.clear()