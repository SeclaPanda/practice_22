import sqlite3, re
from aiogram.types import ReplyKeyboardMarkup
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

def make_kboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    groups = groups_upd()
    for i in groups:
        kb.button(text = f'{i}')
    kb.button(text = '/cancel')
    kb.button(text = '/gr_check')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard = True)

def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text = '/work')
    kb.button(text = '/help')
    kb.button(text = '/cancel')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard = True)

def get_cancel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text = '/cancel')
    kb.adjust()
    return kb.as_markup(resize_keyboard=True, one_time_keyboard = True)