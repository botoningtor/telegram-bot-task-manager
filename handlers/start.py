from aiogram import Router, types
from aiogram.filters import CommandStart
from database import async_session
from services.task_service import get_or_create_user
from keyboards.menu import get_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    async with async_session() as session:
        await get_or_create_user(session, message.from_user.id, message.from_user.username)
    
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я бот-менеджер задач. Используй меню ниже 👇",
        reply_markup=get_main_menu()
    )
