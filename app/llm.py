import httpx
from app.config import API_KEY, LLM_URL


async def call_llm(messages, temperature=0.3):
    """
    apifreellm НЕ поддерживает messages как OpenAI.
    Он принимает ОДНУ строку 'message'.

    Поэтому мы объединяем историю в один текст.
    """

    # Склеиваем историю в один промпт
    full_prompt = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            full_prompt += f"[ИНСТРУКЦИЯ]: {content}\n"
        elif role == "user":
            full_prompt += f"[ПОЛЬЗОВАТЕЛЬ]: {content}\n"
        elif role == "assistant":
            full_prompt += f"[ОТВЕТ]: {content}\n"

    payload = {
        "message": full_prompt,
        # если API поддерживает temperature — можно добавить
        # "temperature": temperature
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            LLM_URL,
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            print("LLM ERROR:", response.text)

        response.raise_for_status()
        data = response.json()

    return data["response"]
