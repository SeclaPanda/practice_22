import sqlite3, re
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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
def make_kboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()
    groups = groups_upd()
    for i in groups:
        markup.button(text = f'{i}')
        markup.adjust(1)
    markup.button(text = 'Новая группа')
    markup.button(text = '/cancel')
    markup.adjust(2)
    return markup.as_markup(resize_keyboard=True, one_time_keyboard = True)