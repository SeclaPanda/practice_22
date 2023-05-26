import sqlite3
from aiogram import Router, F
from aiogram.types import Message
from keyboards.kb_group import groups_upd

router = Router()
conn = sqlite3.connect(r'./groups/groups.db') #подключение и указатель БД 
cur = conn.cursor()
groups = groups_upd()

@router.message(F.text.in_(groups))
#функция регистрации студентов
async def wrt(message: Message):
    registred = False
    for i in groups:
        cur.execute(f'SELECT userid FROM {i} where userid = ?', (str(message.from_user.id),))
        if cur.fetchone() is not None:
            registred = True
            group = i
    if registred == False:    
        query = f'INSERT INTO {message.text} VALUES (\'{str(message.from_user.id)}\', \'{message.from_user.username}\');'
        cur.execute(query)
        conn.commit()
        await message.answer('Отлично! Теперь ты зарегистрирован')
    else:
        await message.answer(f'Хэй! Кажется ты уже зарегестрирован в группе - {group}) Не пытайся меня обмануть, пожалуйста!')