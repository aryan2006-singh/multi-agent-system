"""
llm_client.py
Ek common function jo saare agents use karenge OpenAI GPT ko
call karne ke liye. Isse code repeat nahi karna padta har agent mein.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_llm(system_prompt: str, user_message: str, context: str = "") -> str:
    """
    system_prompt -> agent ka "role" (jaise "tu billing expert hai")
    user_message  -> customer ka actual sawaal
    context       -> RAG se retrieve kiya hua company document text
    """
    full_user_content = user_message
    if context:
        full_user_content = (
            f"Company documents se relevant context:\n{context}\n\n"
            f"Customer ka sawaal: {user_message}\n\n"
            f"Upar diye context ke basis pe jawab do. Agar context mein "
            f"jawab nahi hai to bolo ki tumhe pakka pata nahi, guess mat karo."
        )

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_user_content},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
