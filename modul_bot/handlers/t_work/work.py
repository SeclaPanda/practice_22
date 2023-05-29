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
conn = sqlite3.connect(r'./groups/groups.db') #подключение и указатель БД 
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    snd_group = State()
    text = State()

@router.message(Command('work'))
async def work(message: Message, state: FSMContext):
    await state.set_state(UserState.snd_group)
    await message.answer("""Нажмите на кнопку и выберите группу или отмените данное действие через /cancel 
    \nВы так же можете проверить количество студентов зарегестрированных в группе чтобы свериться со списком и 
быть уверенным, что все студенты зарегестрированы и получат ваше сообщение!""", reply_markup=make_kboard())

@router.message(UserState.snd_group, F.text != '/gr_check') #здесь мы собираем id студентов из группы и сообщение преподавателя
async def snd_msg(message: Message, state: FSMContext):
    if message.text != '/cancel':
        #global num
        num = []
        #await state.update_data(group=message.text)
        #data = await state.get_data()
        query = (f'SELECT userid FROM {message.text};')
        cur.execute(query)
        students = cur.fetchall()
        for i in students:
            i = str(i)
            i = re.sub("[(|)|'|,]","",i)
            num.append(i)
        #print(num)
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
        #await state.update_data(text = message.text)
        #data = await state.get_data()
        #global num
        data = await state.get_data()
        #print(data)
        for i in data['snd_group']:
            print(i)
            with contextlib.suppress(Exception):
                #await router.forward_message(i, message.from_user.id, message.message_id)
                await message.forward(i)#, message.from_user.id, message.message_id)
                print (f'send to {i}')
        await message.answer('Отлично! Ваше сообщение отправлено! Спасибо, что пользуетесь ботом - "Помощник преподавателя"!', reply_markup=get_kb())
    else:
        await cancel.cmd_cancel(message, state)
    await state.clear()