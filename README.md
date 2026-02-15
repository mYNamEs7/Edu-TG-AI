# 🤖 Edu TG AI · [🌐 Demo](https://t.me/eedu_ai_bot)

> Образовательный Telegram-бот с интеграцией искусственного интеллекта — помогает в обучении, объясняет сложные темы и ведёт контекстный диалог.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-2CA5E0?style=flat&logo=telegram&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_API-412991?style=flat&logo=openai&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white)

</div>

---

## 🎯 О проекте

Edu TG AI — это интеллектуальный Telegram-бот, который превращает процесс обучения в интерактивный опыт. Бот использует AI для объяснения сложных тем, помощи с задачами и ведения контекстного диалога.

**Разработано с нуля** — от продумывания пользовательских сценариев и интеграции с AI API до реализации полноценного бота с системой состояний и хранением данных.

---

## 🛠️ Технологический стек

| Направление | Технологии |
|:---|:---|
| **Язык** | Python 3.11+ |
| **Telegram API** | aiogram 3.x |
| **AI-интеграция** | OpenAI API / совместимые LLM |
| **База данных** | PostgreSQL · SQLAlchemy |
| **Архитектура** | FSM (Finite State Machine) · роутеры · middleware |

---

## ⚙️ Ключевые возможности

| Возможность | Описание |
|:---|:---|
| 🧠 **AI-ассистент** | Диалог с ИИ по любой учебной теме — объясняет сложные концепции простым языком |
| 💬 **Контекстный диалог** | Бот запоминает контекст беседы, позволяя вести последовательный диалог с уточняющими вопросами |
| 👤 **Управление пользователями** | Регистрация, хранение истории взаимодействий, персонализация ответов |
| 🔄 **Webhooks** | Асинхронная обработка сообщений для масштабируемости |

---

## 🏗 Архитектура

| Директория | Назначение |
|:---|:---|
| `main.py` | Точка входа, запуск бота |
| `config.py` | Конфигурация (токены, настройки) |
| `database/models.py` | ORM модели |
| `database/database.py` | Подключение к БД |
| `handlers/start.py` | /start, приветствие |
| `handlers/ai_chat.py` | Диалог с AI |
| `services/ai_service.py` | Обёртка над OpenAI API |
| `keyboards/inline.py` | Inline-клавиатуры |
| `keyboards/reply.py` | Reply-клавиатуры |
| `states/states.py` | FSM-состояния |
| `middlewares/auth.py` | Middleware авторизации |

---

## 🚀 Быстрый старт

### Требования

- Python 3.11+
- PostgreSQL
- Telegram Bot Token
- OpenAI API Key

### Установка

    git clone https://github.com/mYNamEs7/Edu-TG-AI.git
    cd Edu-TG-AI
    pip install -r requirements.txt

### Настройка

Создайте <code>.env</code> файл:

    BOT_TOKEN=your_telegram_bot_token
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=postgresql://user:password@localhost/dbname

### Запуск

    python main.py
