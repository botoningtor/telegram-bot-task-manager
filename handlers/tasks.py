from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import async_session
import services.task_service as service
from keyboards.menu import get_tasks_keyboard

router = Router()

class TaskStates(StatesGroup):
    waiting_for_title = State()

# --- Сценарий создания задачи (FSM) ---
@router.message(F.text == "📝 Добавить задачу")
async def process_add_task(message: types.Message, state: FSMContext):
    await state.set_state(TaskStates.waiting_for_title)
    await message.answer("Введите название задачи:")

@router.message(TaskStates.waiting_for_title)
async def save_task_title(message: types.Message, state: FSMContext):
    async with async_session() as session:
        await service.add_task(session, message.from_user.id, message.text)
    
    await state.clear()
    await message.answer(f"Задача «{message.text}» успешно добавлена!")

# --- Просмотр задач ---
@router.message(F.text == "📋 Мои задачи")
async def show_tasks(message: types.Message):
    async with async_session() as session:
        tasks = await service.get_user_tasks(session, message.from_user.id)
    
    if not tasks:
        await message.answer("У вас пока нет задач.")
        return
        
    await message.answer("Ваш список задач:", reply_markup=get_tasks_keyboard(tasks))

# --- CallbackQuery (Изменение статуса и удаление) ---
@router.callback_query(F.data.startswith("toggle_"))
async def handle_toggle_task(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        await service.toggle_task_status(session, task_id)
        tasks = await service.get_user_tasks(session, callback.from_user.id)
        
    await callback.answer("Статус обновлен")
    await callback.message.edit_reply_markup(reply_markup=get_tasks_keyboard(tasks))

@router.callback_query(F.data.startswith("delete_"))
async def handle_delete_task(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        await service.delete_task(session, task_id)
        tasks = await service.get_user_tasks(session, callback.from_user.id)
        
    await callback.answer("Задача удалена")
    if tasks:
        await callback.message.edit_reply_markup(reply_markup=get_tasks_keyboard(tasks))
    else:
        await callback.message.edit_text("У вас пока нет задач.")
