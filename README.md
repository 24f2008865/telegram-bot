# TDS Project 1 Telegram Data Analyst Bot

This project implements Question 5 from TDS 2026 May Project 1. It receives a
Telegram text message, gives the complete conversation to an LLM, and replies
with exactly one JSON object:

```json
{"answer": <value requested by the question>, "log_url": "https://.../logs/<id>.jsonl"}
```

The model is instructed to return only the `answer` value. The Python service
adds `log_url` itself, which makes the output contract more reliable.

## Security first

The API key shared in the Codex chat must be revoked and replaced before use.
Never commit keys to GitHub. Add the replacement key only as a deployment
environment variable.

## Local test

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Set the variables in the current shell or with a local .env loader.
uvicorn app:app --reload --port 8000
```

For a local webhook, use a public HTTPS tunnel such as Cloudflare Tunnel or
ngrok and set `PUBLIC_BASE_URL` to that HTTPS URL. Then run:

```powershell
python set_webhook.py
```

## Deploy on Render

1. Create a new public GitHub repository and upload this folder.
2. In Render, create a Web Service from that repository. `render.yaml` contains
   the build, start, and health-check settings.
3. Set these environment variables in Render:
   - `OPENAI_API_KEY`: a newly created replacement key
   - `TELEGRAM_BOT_TOKEN`: the token from BotFather
   - `PUBLIC_BASE_URL`: the Render URL, for example `https://name.onrender.com`
   - `TELEGRAM_WEBHOOK_SECRET`: any long random string
   - `OPENAI_MODEL`: `gpt-5-mini` or another model available to your API account
4. Deploy. Startup automatically registers Telegram's webhook at
   `PUBLIC_BASE_URL/webhook`.
5. Message the bot from a normal Telegram user account. Telegram bots cannot
   message another bot, so the grader uses a real user account.

The grading pipeline expects the GitHub URL and Telegram username in the
question's two registration fields. The username must end in `bot`.

## Gemini fallback

If OpenAI API quota is unavailable, set these Render variables instead:

- `GEMINI_API_KEY`: a Google AI Studio API key
- `GEMINI_MODEL`: `gemini-2.5-flash-lite`
- `GEMINI_BASE_URL`: optional. Use `https://aipipe.org/geminiv1beta` for
  AI Pipe `AQ...` tokens.

When `GEMINI_API_KEY` is present, the service uses Gemini and ignores the OpenAI
settings for model calls. Keep `TELEGRAM_BOT_TOKEN` and `PUBLIC_BASE_URL`
configured the same way.

## Reliability notes

The service stores logs on its local filesystem and exposes each run through a
public `/logs/<id>.jsonl` route. This is sufficient while the Render instance
is alive during grading. For maximum reliability, use a non-sleeping Render
plan; the free plan can spin down after inactivity. Telegram retries webhook
delivery if the service is unavailable.

The short in-memory history supports multi-turn grading messages. A redeploy
clears that history, so deploy before testing and leave the service running.
