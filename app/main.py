import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update, BotCommand
from app.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL
from app.handlers import router
from app.database import engine, Base

app = FastAPI()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


@app.on_event("startup")
async def on_startup():
    # создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print(WEBHOOK_URL)
    # удаляем старый webhook
    await bot.delete_webhook()

    # устанавливаем новый
    await bot.set_webhook(WEBHOOK_URL, allowed_updates=["message", "callback_query"])

    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="restart", description="Перезапустить бота"),
        BotCommand(command="mode", description="Выбрать режим работы"),
    ])

    await bot.set_my_description(
        description=(
            "🎓 Образование с нейросетью\n\n"
            "Помогаю:\n"
            "• Решать задачи\n"
            "• Готовиться к экзаменам\n"
            "• Писать курсовые и дипломные\n"
            "• Давать краткие и развернутые ответы\n\n"
            "Нажмите /start чтобы начать 🚀"
        )
    )

    await bot.set_my_short_description(
        short_description="ИИ-помощник для учебы 🎓"
    )

    print("Webhook set to:", WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()


@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    print("Webhook Handler...")
    return {"status": "ok"}
