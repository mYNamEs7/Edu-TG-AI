from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message as TgMessage
from aiogram.filters import Command, CommandStart
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import User, Message
from app.pipeline import generate_answer
from app.modes import MODE_DESCRIPTIONS
import re

router = Router()

@router.message(CommandStart())
async def cmd_start(message: TgMessage):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Выбрать режим", callback_data="go_mode")]
        ]
    )

    text = (
        "<b>🎓 ОБРАЗОВАНИЕ С НЕЙРОСЕТЬЮ</b>\n"
        "━━━━━━━━━━━━━━━\n\n"
        f"Привет, <b>{message.from_user.first_name}</b> 👋\n\n"
        "Я — твой интеллектуальный помощник.\n\n"
        "<b>Доступные режимы:</b>\n"
        "📚 exam — подготовка к экзаменам\n"
        "🏛 university — университетский стиль\n"
        "🎓 thesis — научный стиль\n"
        "✏ short — краткие ответы\n\n"
        "Нажми кнопку ниже, чтобы выбрать режим 👇"
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

@router.message(Command("start"))
async def cmd_start(message: TgMessage):
    await message.answer(
        "Привет!\nЯ - нейросеть, помогающая студентам.\nИспользуй меню команд или напиши /mode, чтобы выбрать режим.\nРежим по умолчанию - Экзамен"
    )

@router.message(Command("restart"))
async def cmd_restart(message: TgMessage):
    user_id = str(message.from_user.id)

    async with AsyncSessionLocal() as session:
        # Находим пользователя
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("История пуста.")
            return

        # Удаляем все сообщения пользователя
        await session.execute(
            Message.__table__.delete().where(Message.user_id == user.id)
        )

        await session.commit()

    await message.answer("История диалога очищена. Начинаем с чистого листа ✅")

@router.message(Command("mode"))
async def cmd_mode(message: TgMessage):
    await mode_selection(message=message)

async def mode_selection(message: TgMessage):
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

@router.callback_query(lambda c: c.data == "go_mode")
async def go_mode(callback: CallbackQuery):
    await callback.message.answer("/mode")
    await mode_selection(message=callback.message)

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

        answer = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", answer)
        await message.answer(answer, parse_mode="HTML")
