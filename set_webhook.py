import os

import httpx


token = os.environ["TELEGRAM_BOT_TOKEN"]
base_url = os.environ["PUBLIC_BASE_URL"].rstrip("/")
payload = {"url": f"{base_url}/webhook"}
secret = os.environ.get("TELEGRAM_WEBHOOK_SECRET")
if secret:
    payload["secret_token"] = secret

response = httpx.post(
    f"https://api.telegram.org/bot{token}/setWebhook",
    json=payload,
    timeout=30,
)
response.raise_for_status()
print(response.json())
