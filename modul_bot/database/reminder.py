import sqlite3, re
from aiogram import Router
from aiogram.types import Message
from datetime import datetime
from keyboards.kb_group import groups_upd

conn = sqlite3.connect(r'./modul_bot/database/groups.db') #подключение и указатель БД 
cur = conn.cursor()

async def reminder(bot): #напоминалка всем студентам что база скоро очистится
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