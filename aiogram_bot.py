import contextlib
import logging
import re
import sqlite3
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncio import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Объект бота 
bot = Bot(token='5432818658:AAHNCv2cCmy9f2L5aoxgJInct_kP0fZrvvk')
# Диспетчер для бота
dp = Dispatcher(bot, storage = MemoryStorage())
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# объект расписания
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

class UserState(StatesGroup): #передача переменных 
    group = State()
    text = State()
    group_reg = State()
    n_group = State()

conn = sqlite3.connect(r'./groups/groups.db') #подключение и указатель БД 
cur = conn.cursor()

def groups_upd(): #функция для обновления списка групп
    groups = []
    cur.execute('''SELECT tbl_name FROM sqlite_master WHERE type = 'table';''')
    files = (cur.fetchall())
    for i in files:
        i = str(i)
        i = re.sub("[(|)|'|,]","",i)
        groups.append(i)
    return groups

#функция генерации кнопок с названиями групп
def make_kboard(markup):
    groups = groups_upd()
    for i in groups:
        i = types.KeyboardButton(f'{i}')
        markup.add(i)

#"стартовая" панель бота
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    with open ('./annotation/start.txt', encoding="utf-8") as s:
        content = s.read()
    await message.reply(content)
    await sleep(1)
    await message.answer('Если вы студент вам необходимо только зарегистрироваться - /reg')
    await sleep(1)
    f = './id.txt'
    with open(f, "a") as myfile:
        your_variable = (f'{str(message.from_user.id)} - {str(message.from_user.username)}'+ '\n')
        myfile.write(your_variable)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = "/work")
    btn2 = types.KeyboardButton(text = "/help")
    btn3 = types.KeyboardButton(text = "/reg")
    markup.add(btn1, btn2, btn3)
    await message.answer('Для начала работы от лица преподавателя и выбора группы напишите или нажите - /work', reply_markup=markup)

async def cancel_work(message): #функция отмены выбранного действия преподователем
    with open ('./annotation/cancel_work.txt', encoding="utf-8") as h:
        content = h.read()
    await message.answer(content)

#панель работы преподавателя
@dp.message_handler(commands=['work'])
async def work(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(text = "/cancel")
    btn2 = types.KeyboardButton(text = "/gr_check")
    markup.add(btn1, btn2)
    make_kboard(markup)
    await message.answer("""Нажмите на кнопку и выберите группу или отмените данное действие через /cancel 
    \nВы так же можете проверить количество студентов зарегестрированных в группе чтобы свериться со списком и 
быть уверенным, что все студенты зарегестрированы и получат ваше сообщение!""", reply_markup=markup)
    await UserState.group.set()

    @dp.message_handler(state=UserState.group) #здесь мы собираем id студентов из группы и сообщение преподавателя
    async def snd_msg(message: types.message, state: FSMContext):
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
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text = "/work")
            btn2 = types.KeyboardButton(text = "/cancel")
            btn3 = types.KeyboardButton(text = "/help")
            markup.add(btn1, btn2, btn3)
            await message.answer(content, reply_markup=markup)

        #отправка сообщения преподавателя
        @dp.message_handler(state=UserState.text)
        async def snd(message: types.Message, state: FSMContext):
            if message.text != '/cancel':
                await state.update_data(text=message.text)
                data = await state.get_data()
                global num
                for i in num:
                    with contextlib.suppress(Exception):
                        await bot.forward_message(i, message.from_user.id, message.message_id)
            else:
                await cancel_work(message)
            await message.answer('Отлично! Ваше сообщение отправлено! Спасибо, что пользуетесь ботом - "Помощник преподавателя"!')
            await state.finish()

#регистрационная панель студентов в группы
@dp.message_handler(commands='reg',  content_types='text')
async def reg(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Новая группа')
    btn2 = types.KeyboardButton('/cancel')
    markup.add(btn1, btn2)
    make_kboard(markup)
    await message.answer("Нажми на кнопку и выбери группу ", reply_markup=markup)
    await UserState.group_reg.set()

    @dp.message_handler(state=UserState.group_reg) #проверяем что выбрали студенты на панели регистрации
    async def check(message: types.message, state: FSMContext):
        groups = groups_upd()
        await state.update_data(group_reg=message.text)
        data = await state.get_data()
        if data['group_reg'] in ['Новая группа', btn1]:
            await ngr(message)
        elif data['group_reg'] not in groups:
            await help(message) if data['group_reg'] == '/cancel' else await help(message)
            await state.finish()
        else:
            await wrt(data['group_reg'], message)
            await state.finish()

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

    async def ngr(message: types.Message): #сбор названия новой группы
        await message.answer('введите номер группы в формате: uis_111')
        await UserState.n_group.set()

    @dp.message_handler(state=UserState.n_group) #функция создания новой группы
    async def ntxt(message: types.Message, state: FSMContext):
        await state.update_data(n_group=message.text)
        data = await state.get_data()
        query = (
            'CREATE TABLE IF NOT EXISTS '
            + data['n_group']
            + ' (userid TEXT PRIMARY KEY, nickname TEXT);'
        )
        cur.execute(query)
        conn.commit()
        await message.reply('Отлично!  Группа создана! Теперь вернемся через /reg и зарегистрируемся в неё! ЖМИ!')
        await state.finish()

@dp.message_handler(commands='help') #функция вывода справки 
async def help(message: types.Message):
    with open ('./annotation/help.txt', encoding="utf-8") as h:
        content = h.read()
    await message.answer(content)

@dp.message_handler(commands='reg_help') #функция вывода справки по регистрации
async def reg_help(message: types.Message):
    with open ('./annotation/reg_help.txt', encoding="utf-8") as h:
        content = h.read()
    await message.answer(content)

@dp.message_handler(commands='del_reg')#функция удаления зарегестрированного студента
async def del_reg(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text = "/yes")
    btn2 = types.KeyboardButton(text = "/no")
    markup.add(btn1, btn2)
    await message.answer('Вы уверены что хотите удалить себя из базы данных? Предупреждаю, что после этого вы можете пропустить важное сообщение от преподавателя!', reply_markup=markup)

    @dp.message_handler()
    async def yes(message: types.Message):    
        if message.text == 'yes' or 'да' or '/yes':
            groups = groups_upd()
            for i in groups:
                cur.execute(f'SELECT userid FROM {i} where userid = ?', (str(message.from_user.id),))
                if cur.fetchone() is not None:
                    group = i
            cur.execute(f'DELETE FROM {group} where userid = ?', (str(message.from_user.id),))
            conn.commit()
            await message.answer('Жаль, конечно, но что поделать! Теперь ты удален из моей баззы данных:( Возвращайся!')
        else:
            await message.answer('Вот и славно) Рад, что ты остаешься с нами!')

@dp.message_handler(commands='gr_check') #функция проверки количества студентов в группе
async def gr_check(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    make_kboard(markup)
    await message.answer('Выберите группу которую хотите проверить на количество зарегестрированных студентов', reply_markup=markup)
    
    @dp.message_handler()# вывод кол-ва студентов в группе
    async def gr(message: types.Message):
        cur.execute(f"select count(*) from {message.text}")
        row_count = cur.fetchone()
        await message.answer(f'Количество студентов в группе {message.text} равно {row_count[0]}')
        await message.answer(f'Моежете вернуться к отправке сообщений студентам с помощью команды /work \nИли же прочитать справку через команду /help ')

#функция для очистки базы данных
async def clean():
    groups = groups_upd()
    for i in groups:    
        cur.execute(f'DROP TABLE IF EXISTS {i};')
    print(f"База данных была сброшена! Не забудьте сказать студентам, что пора регестрироваться снова! {datetime.now().strftime('%d - %m - %Y')}!")

async def reminder(): #напоминалка всем студентам что база скоро очистится
    num = []
    groups = groups_upd()
    for i in groups:
        query = f'SELECT userid FROM {i};'
        cur.execute(query)
        students = cur.fetchall()
        for i in students:
            i = str(i)
            i = re.sub("[(|)|'|,]","",i)
            num.append(i)
    for i in num:
        await bot.send_message(i, '''Не забывайте, что сегодня в 18:00 база данных будет очищена. 
Необходимо будет зарегестрироваться в группах заново! Спасибо.''')

#создание расписания на удаление студентов из базы данных в начале первого и второго семестров
scheduler.add_job(clean, 'cron', day = 1, month = 2, hour = 18, id='job_1')
scheduler.add_job(clean, 'cron', day = 20, month = 8, hour = 18, id='job_2')
#создание расписания напоминания студентам зарегестрироваться в группах заново 
scheduler.add_job(reminder, 'cron', day = 1, month = 2, hour = 17, minute = 30, id='job_3')
scheduler.add_job(reminder, 'cron', day = 20, month = 8, hour = 17, minute = 30, id='job_4')

if __name__ == '__main__':
    # Запуск расписания для удалений
    scheduler.start()
    # Запуск бота
    executor.start_polling(dp, skip_updates=True) 