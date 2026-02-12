from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message as TgMessage
from aiogram.filters import Command
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import User, Message
from app.pipeline import generate_answer
from app.modes import MODE_DESCRIPTIONS
import re

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет!\nЯ - нейросеть, помогающая студентам.\nИспользуй меню команд или напиши /mode, чтобы выбрать режим.\nРежим по умолчанию - exam"
    )

@router.message(Command("mode"))
async def cmd_mode(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=mode, callback_data=f"mode:{mode}")]
            for mode in MODE_DESCRIPTIONS
        ]
    )
    await message.answer(
        "Выберите режим работы бота:",
        reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data and c.data.startswith("mode:"))
async def mode_callback(callback: CallbackQuery):
    mode = callback.data.split(":")[1]
    text_to_send = f"/mode {mode}"
    
    await change_mode(mode=mode, user_id=callback.message.from_user.id)
    
    await callback.message.answer(f"Вы выбрали: {text_to_send}\n{MODE_DESCRIPTIONS[mode]}")

    await callback.message.edit_reply_markup(reply_markup=None)

async def change_mode(mode: str, user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == str(user_id))
        )
        user = result.scalar_one_or_none()

        if user:
            user.mode = mode
            await session.commit()

@router.message()
async def handle_message(message: TgMessage):
    await message.answer(f"Сообщение принято в обработку...\nНейросеть скоро ответит!")
    
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

        answer = answer.replace("\\", "").replace("\\times", "*").replace("")
        answer = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", answer)
        await message.answer(answer, parse_mode="HTML")
