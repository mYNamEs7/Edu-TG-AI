from app.llm import call_llm
from app.modes import MODES, DEFAULT_PROPT


async def generate_answer(user_input, mode, history):
    """
    Упрощённая версия без двойного запроса,
    чтобы не ловить 429.
    """
    
    system_prompt = DEFAULT_PROPT + MODES.get(mode, MODES["exam"])

    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": user_input}
    ]
    
    answer = await call_llm(messages)

    return answer
