import contextlib, sqlite3, re
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text
from aiogram.methods import ForwardMessage
from keyboards.work_kb import make_kboard, get_kb, get_cancel
from handlers import cancel
from handlers.t_work import gr_check

router = Router()
router.include_routers(gr_check.router)#, n_group.router , wrt.router)

conn = sqlite3.connect(r'./modul_bot/database/groups.db') #подключение и указатель БД  modul_bot/database modul_bot\database
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    snd_group = State()
    text = State()
    passw = State()

@router.message(Command('work'))
async def ent_passw(message: Message, state: FSMContext):
    await message.answer("""Введите пароль для работы от лица преподавателя: 
Вы всегда можете отменить действие командой /cancel""")
    await state.set_state(UserState.passw)
    print(UserState.passw)    

@router.message(UserState.passw)
async def auth(message: Message, state: FSMContext):
    await state.update_data(passw = message.text)
    data = await state.get_data()
    if data['passw'] == '1520':
        await state.set_state(UserState.snd_group)
        await message.answer("""Выберите группу которой хотите отправить сообщение или отмените данное действие через /cancel 
\nВы так же можете проверить количество студентов зарегистрированных в группе с помощью команды /gr_check чтобы свериться со списком и 
быть уверенным, что все студенты зарегестрированы и получат ваше сообщение!""", reply_markup=make_kboard())
    else:
        await state.set_state(UserState.passw)
        await message.answer("""К сожалению это не правильный пароль! Если вы забыли или еще не знаете его - обратитесь к администратору.
Так же вы можете отменить текущее действие командой - /cancel""")

@router.message(UserState.snd_group, F.text != '/gr_check') #здесь мы собираем id студентов из группы и сообщение преподавателя
async def snd_msg(message: Message, state: FSMContext):
    if message.text != '/cancel':
        num = []
        query = (f'SELECT userid FROM "{message.text}";')
        cur.execute(query)
        students = cur.fetchall()
        for i in students:
            i = str(i)
            i = re.sub("[(|)|'|,]","",i)
            num.append(i)
        await state.update_data(snd_group = num)
        await state.set_state(UserState.text)
        await message.answer('Введите текст для отправки: ')
        with open ('./annotation/after_work.txt', encoding="utf-8") as a_w:
            content = a_w.read()
        await message.answer(content, reply_markup=get_cancel())
    else:
        await cancel.cmd_cancel(message, state)

#отправка сообщения преподавателя
@router.message(UserState.text)
async def snd(message: Message, state: FSMContext):
    if message.text != '/cancel':
        data = await state.get_data()
        for i in data['snd_group']:
            with contextlib.suppress(Exception):
                await message.forward(i)
        await message.answer('Отлично! Ваше сообщение отправлено! Спасибо, что пользуетесь ботом - "Помощник преподавателя"!', reply_markup=get_kb())
    else:
        await cancel.cmd_cancel(message, state)
    await state.clear()