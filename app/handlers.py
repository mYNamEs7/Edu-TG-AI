from aiogram import Router, F
from aiogram.types import Message as TgMessage
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import User, Message
from app.pipeline import generate_answer

router = Router()

@router.message(F.text.startswith("/mode"))
async def change_mode(message: TgMessage):
    mode = message.text.split(" ")[1]

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == str(message.from_user.id))
        )
        user = result.scalar_one_or_none()

        if user:
            user.mode = mode
            await session.commit()

    await message.answer(f"Режим изменен на {mode}")

@router.message()
async def handle_message(message: TgMessage):
    await message.answer(f"Ты написал: {message.text}")
    
    async with AsyncSessionLocal() as session:

        result = await session.execute(
            select(User).where(User.telegram_id == str(message.from_user.id))
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(telegram_id=str(message.from_user.id))
            session.add(user)
            await session.commit()

        history_query = await session.execute(
            select(Message).where(Message.user_id == user.id)
        )
        history = history_query.scalars().all()

        history_formatted = [
            {"role": msg.role, "content": msg.content}
            for msg in history[-10:]
        ]

        answer = await generate_answer(
            message.text,
            user.mode,
            history_formatted
        )

        session.add(Message(user_id=user.id, role="user", content=message.text))
        session.add(Message(user_id=user.id, role="assistant", content=answer))
        await session.commit()

        await message.answer(answer)
