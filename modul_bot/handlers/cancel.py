from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Text
from handlers import help

router = Router()

@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
@router.callback_query(F.data == 'cancel')
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
    await help.help(message)