import contextlib, sqlite3, re
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, Text
from keyboards.kb_group import make_kboard

router = Router()

conn = sqlite3.connect(r'./groups/groups.db') #подключение и указатель БД 
cur = conn.cursor()

class UserState(StatesGroup): #передача переменных 
    group = State()
    text = State()

@router.message(Command('work'))
async def work(message: Message, state: FSMContext):
    markup = ReplyKeyboardMarkup()
    btn1 = KeyboardButton(text = "/cancel")
    btn2 = KeyboardButton(text = "/gr_check")
    markup.add(btn1, btn2)
    make_kboard(markup)
    await message.answer("""Нажмите на кнопку и выберите группу или отмените данное действие через /cancel 
    \nВы так же можете проверить количество студентов зарегестрированных в группе чтобы свериться со списком и 
быть уверенным, что все студенты зарегестрированы и получат ваше сообщение!""", reply_markup=markup)
    await UserState.group.set()

    @router.message(state=UserState.group) #здесь мы собираем id студентов из группы и сообщение преподавателя
    async def snd_msg(message: message, state: FSMContext):
        global num
        num = []
        await state.update_data(group=message.text)
        data = await state.get_data()
        if message.text == '/cancel':
            await cancel_work(message)
            await state.finish()
        elif message.text == '/gr_check':
            await gr_check(message)
            await state.finish()
        else:
            query = f'SELECT userid FROM {message.text};'
            cur.execute(query)
            students = cur.fetchall()
            for i in students:
                i = str(i)
                i = re.sub("[(|)|'|,]","",i)
                num.append(i)
            await message.answer('Введите текст для отправки: ')
            await UserState.text.set()
            with open ('./annotation/after_work.txt', encoding="utf-8") as a_w:
                content = a_w.read()
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton(text = "/work")
            btn2 = KeyboardButton(text = "/cancel")
            btn3 = KeyboardButton(text = "/help")
            markup.add(btn1, btn2, btn3)
            await message.answer(content, reply_markup=markup)

        #отправка сообщения преподавателя
        @router.message(state=UserState.text)
        async def snd(message: Message, state: FSMContext):
            if message.text != '/cancel':
                await state.update_data(text=message.text)
                data = await state.get_data()
                global num
                for i in num:
                    with contextlib.suppress(Exception):
                        await message.forward_message(i, message.from_user.id, message.message_id)
            else:
                await cancel_work(message)
            await message.answer('Отлично! Ваше сообщение отправлено! Спасибо, что пользуетесь ботом - "Помощник преподавателя"!')
            await state.finish()

@router.message(Command('gr_check')) #функция проверки количества студентов в группе
async def gr_check(message: Message):
    markup = ReplyKeyboardMarkup()
    make_kboard(markup)
    await message.answer('Выберите группу которую хотите проверить на количество зарегестрированных студентов', reply_markup=markup)
    
    @router.message()# вывод кол-ва студентов в группе
    async def gr(message: Message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = KeyboardButton(text = "/work")
        btn2 = KeyboardButton(text = "/help")
        markup.add(btn1, btn2)
        cur.execute(f"select count(*) from {message.text}")
        row_count = cur.fetchone()
        await message.answer(f'Количество студентов в группе {message.text} равно {row_count[0]}')
        await message.answer(f'Моежете вернуться к отправке сообщений студентам с помощью команды /work \nИли же прочитать справку через команду /help', reply_markup=markup)

async def cancel_work(message): #функция отмены выбранного действия преподователем
    with open ('./annotation/cancel_work.txt', encoding="utf-8") as h:
        content = h.read()
    await message.answer(content)