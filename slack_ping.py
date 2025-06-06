import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#ai-results")

message = "✅ Hi from Jenkins (no screenshots, just a plain message)"

response = requests.post(
    "https://slack.com/api/chat.postMessage",
    headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
    json={"channel": SLACK_CHANNEL, "text": message}
)

if response.status_code == 200 and response.json().get("ok"):
    print("✅ Message sent to Slack.")
else:
    print("❌ Failed to send message:", response.text)
