import contextlib, sqlite3
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
import sqlite3
from keyboards.kb_group import make_kboard, groups_upd
from handlers import help

router = Router()
@router.message(Command('cancel'))
async def cancel(message: Message):
    await help.help(message)