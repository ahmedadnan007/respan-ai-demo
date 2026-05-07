# AI Customer Support Bot - Respan (Keywords AI) Demo

A small Python demo that routes chat completions through Respan so you can monitor requests, tokens, spend, latency, and errors from one dashboard.

## What This Demo Shows

- Proxying model calls through Respan
- Using a Gemini model via Respan's model mapping
- Sending a custom `customer_identifier` for trace grouping
- Viewing logs and observability metrics in real time

## Prerequisites

- A Respan account and project on [keywordsai.co](https://keywordsai.co)
- A Gemini API key (for provider setup inside Respan)

## Setup

### 1. Configure Respan Dashboard

1. Create a project in Respan.
2. Add your Gemini provider key in `Settings -> Providers`.
3. Add a model in `Platform -> Models`.
4. Use the exact model ID from that list (example: `gemini/gemini-2.5-flash`).

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create/update `.env`:

```env
KEYWORDSAI_API_KEY=your-respan-api-key
MODEL_NAME=gemini/gemini-2.5-flash
ORG_ID=your-org-id
```

Notes:
- `MODEL_NAME` must exactly match the model ID from your Respan Models page.
- `ORG_ID` is optional for this script but useful for reporting/sharing.

### 4. Run

```bash
python demo.py
```

## Expected Output

The script sends three customer-support style prompts and prints responses.

Each request appears in Respan logs with observability data such as:
- Request count
- Token usage
- Spend
- Error rate and latency

## Files

- `demo.py`: main runnable script
- `requirements.txt`: Python dependencies
- `.env`: local secrets and model config (ignored by git)
