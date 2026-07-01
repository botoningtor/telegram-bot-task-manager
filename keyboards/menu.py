from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Добавить задачу")],
            [KeyboardButton(text="📋 Мои задачи")]
        ],
        resize_keyboard=True
    )

def get_tasks_keyboard(tasks: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for task in tasks:
        status_icon = "✅" if task.completed else "❌"
        
        # 1. Кнопка с текстом задачи. Вместо url используем безопасный callback_data, который ничего не делает при нажатии
        builder.row(
            InlineKeyboardButton(
                text=f"{status_icon} {task.title}", 
                callback_data=f"none_{task.id}"  # Безопасная заглушка
            )
        )
        # 2. Кнопки управления этой задачей (под текстом)
        builder.row(
            InlineKeyboardButton(text="🔄 Статус", callback_data=f"toggle_{task.id}"),
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{task.id}")
        )
        
    return builder.as_markup()
