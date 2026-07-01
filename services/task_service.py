from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Task

async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str | None) -> User:
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user

async def add_task(session: AsyncSession, telegram_id: int, title: str) -> None:
    user = await get_or_create_user(session, telegram_id, None)
    task = Task(user_id=user.id, title=title)
    session.add(task)
    await session.commit()

async def get_user_tasks(session: AsyncSession, telegram_id: int) -> list[Task]:
    query = select(Task).join(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    return list(result.scalars().all())

async def toggle_task_status(session: AsyncSession, task_id: int) -> None:
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if task:
        task.completed = not task.completed
        await session.commit()

async def delete_task(session: AsyncSession, task_id: int) -> None:
    statement = delete(Task).where(Task.id == task_id)
    await session.execute(statement)
    await session.commit()
