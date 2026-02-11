import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL").replace(
    "postgresql://",
    "postgresql+asyncpg://"
)

BASE_URL = os.getenv("BASE_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

LLM_URL = "https://apifreellm.com/api/v1/chat"
