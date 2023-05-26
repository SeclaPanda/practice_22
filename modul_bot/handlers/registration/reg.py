from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.kb_group import make_kboard
from handlers.registration import n_group, wrt, cancel, del_reg

router = Router()
router.include_routers(n_group.router, wrt.router, cancel.router, del_reg.router)

#регистрационная панель студентов в группы
@router.message(Command('reg'))
async def reg(message: Message):
    await message.answer("Нажми на кнопку и выбери группу ", reply_markup=make_kboard())