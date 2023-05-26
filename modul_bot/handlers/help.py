import contextlib, sqlite3
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
import sqlite3
from keyboards.kb_group import make_kboard, groups_upd

router = Router()
@router.message(Command('help')) #функция вывода справки 
async def help(message: Message):
    with open ('./annotation/help.txt', encoding="utf-8") as h:
        content = h.read()
    await message.answer(content)