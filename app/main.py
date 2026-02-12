import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from app.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL
from app.handlers import router
from app.database import engine, Base

app = FastAPI()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
print("hello 1")


@app.on_event("startup")
async def on_startup():
    print("hello 11")
    # создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # удаляем старый webhook
    await bot.delete_webhook()

    # устанавливаем новый
    await bot.set_webhook(WEBHOOK_URL)

    print("Webhook set to:", WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    print("hello 111")
    await bot.delete_webhook()
    await bot.session.close()


@app.post("/webhook")
async def webhook_handler(request: Request):
    print("hello 11111")
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}
