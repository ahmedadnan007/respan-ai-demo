# AI Customer Support Bot - Keywords AI Demo

A simple demo showcasing how to use Keywords AI (Respan) to monitor and observe OpenAI API calls in real-time.

## What This Does

This demo builds a basic AI customer support bot that routes requests through Keywords AI instead of calling OpenAI directly. This allows you to:

- See all API calls in the Keywords AI dashboard
- Monitor costs per call
- Track response times
- View full conversation logs

## Setup

### 1. Create a Keywords AI Account
- Go to [keywordsai.co](https://keywordsai.co)
- Create a free account
- Create a new Project
- Copy your **API Key** and **Organization ID**

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Update the `.env` file with your actual Keys:
```
KEYWORDSAI_API_KEY=your-actual-keywords-ai-key
OPENAI_API_KEY=your-actual-openai-key
ORG_ID=your-actual-org-id
```

### 4. Run the Demo
```bash
python demo.py
```

Each call will be logged in your Keywords AI dashboard in real-time.

## How It Works

This demo uses **Google Gemini API** to power the customer support bot:

```python
import google.generativeai as genai

genai.configure(api_key="your-gemini-api-key")
model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Your question here...")
```

Simple, fast, and integrated with Keywords AI for observability.

## Viewing Your Logs

1. Run `python demo.py` multiple times
2. Go to your Keywords AI dashboard
3. See all calls, costs, and response times
