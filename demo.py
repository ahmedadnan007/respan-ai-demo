from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

KEYWORDSAI_BASE_URL = "https://api.keywordsai.co/api/"
MODEL_NAME = os.getenv("MODEL_NAME", "gemini/gemini-2.5-flash")

_default_client = None


def _get_client():
    global _default_client
    if _default_client is None:
        _default_client = OpenAI(
            api_key=os.getenv("KEYWORDSAI_API_KEY"),
            base_url=KEYWORDSAI_BASE_URL,
        )
    return _default_client


def chat(user_message, client=None):
    """Send a message to the AI customer support bot through Keywords AI."""
    c = client if client is not None else _get_client()
    response = c.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": user_message},
        ],
        extra_body={"customer_identifier": "demo-support-bot"},
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("Running AI Customer Support Bot Demo with Keywords AI...\n")

    print("Q: What is your return policy?")
    print(f"A: {chat('What is your return policy?')}\n")

    print("Q: How do I track my order?")
    print(f"A: {chat('How do I track my order?')}\n")

    print("Q: Can I change my delivery address?")
    print(f"A: {chat('Can I change my delivery address?')}\n")
