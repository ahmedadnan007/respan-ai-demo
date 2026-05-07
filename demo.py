import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini API
client = genai.Client(api_key=os.getenv("OPENAI_API_KEY"))

def chat(user_message):
    """Send a message to the AI customer support bot."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"You are a helpful customer support assistant. Please answer this question: {user_message}"
    )
    return response.text

# Test it
if __name__ == "__main__":
    print("Running AI Customer Support Bot Demo with Gemini...\n")
    
    print("Q: What is your return policy?")
    print(f"A: {chat('What is your return policy?')}\n")
    
    print("Q: How do I track my order?")
    print(f"A: {chat('How do I track my order?')}\n")
    
    print("Q: Can I change my delivery address?")
    print(f"A: {chat('Can I change my delivery address?')}\n")
