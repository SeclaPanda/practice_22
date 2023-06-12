import sqlite3, re
from aiogram import Router
from aiogram.types import Message
from datetime import datetime
from keyboards.kb_group import groups_upd

conn = sqlite3.connect(r'./modul_bot/database/groups.db') #подключение и указатель БД 
cur = conn.cursor()

#функция для очистки базы данных
async def clean():
    groups = groups_upd()
    for i in groups:    
        cur.execute(f'DROP TABLE IF EXISTS {i};')
    print(f"База данных была сброшена! Не забудьте сказать студентам, что пора регистрироваться снова! {datetime.now().strftime('%d - %m - %Y')}!")