from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Configure to use Keywords AI as proxy
client = OpenAI(
    api_key=os.getenv("KEYWORDSAI_API_KEY"),
    base_url="https://api.keywordsai.co/api/"
)

MODEL_NAME = os.getenv("MODEL_NAME", "gemini/gemini-2.5-flash")

def chat(user_message):
    """Send a message to the AI customer support bot through Keywords AI."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful customer support assistant."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        extra_body={
            "customer_identifier": "demo-support-bot",
        }
    )
    return response.choices[0].message.content

# Test it
if __name__ == "__main__":
    print("Running AI Customer Support Bot Demo with Keywords AI...\n")
    
    print("Q: What is your return policy?")
    print(f"A: {chat('What is your return policy?')}\n")
    
    print("Q: How do I track my order?")
    print(f"A: {chat('How do I track my order?')}\n")
    
    print("Q: Can I change my delivery address?")
    print(f"A: {chat('Can I change my delivery address?')}\n")
