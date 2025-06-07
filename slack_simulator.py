# #hi message: This script merges screenshots from a folder and sends the result to a Slack channel.


# import os
# import requests
# from PIL import Image
# from dotenv import load_dotenv

# load_dotenv()

# SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#ai-results")

# FALLBACK_IMAGE = "fallback.png"

# def merge_screenshots(input_folder, output_path):
#     if not os.path.exists(input_folder) or not os.listdir(input_folder):
#         print("⚠️ Folder not found: screenshots. Using fallback image.")
#         return FALLBACK_IMAGE

#     files = sorted([f for f in os.listdir(input_folder) if f.endswith(".png")])
#     if not files:
#         print("⚠️ No PNGs in screenshots. Using fallback image.")
#         return FALLBACK_IMAGE

#     images = [Image.open(os.path.join(input_folder, f)) for f in files]
#     widths, heights = zip(*(img.size for img in images))
#     total_height = sum(heights)
#     max_width = max(widths)

#     combined = Image.new("RGB", (max_width, total_height))
#     y_offset = 0
#     for img in images:
#         combined.paste(img, (0, y_offset))
#         y_offset += img.size[1]

#     combined.save(output_path)
#     print(f"✅ Combined screenshot saved to {output_path}")
#     return output_path

# def send_to_slack(text, image_path, report_url=None):
#     try:
#         with open(image_path, "rb") as f:
#             response = requests.post(
#                 "https://slack.com/api/files.upload",
#                 headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
#                 files={"file": f},
#                 data={
#                     "channels": SLACK_CHANNEL,
#                     "initial_comment": f"{text}\n{report_url or ''}"
#                 }
#             )
#         if response.status_code == 200 and response.json().get("ok"):
#             print("✅ Report sent to Slack.")
#         else:
#             print("❌ Failed to upload image:", response.text)
#     except Exception as e:
#         print(f"❌ Exception during Slack upload: {e}")

# if __name__ == "__main__":
#     image = merge_screenshots("screenshots", "screenshots/combined.png")
#     status = "✅ PASS" if image != FALLBACK_IMAGE else "❌ FAIL"
#     send_to_slack(
#         text=f"{status} - AI UI Test Result",
#         image_path=image,
#         report_url="https://jenkins.yoursite.com/job/AI%20UI%20Test%20Bot/"
#     )


import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#ai-results")

fallback_image_path = "fallback.png"

def send_image_with_message(image_path, message):
    if not os.path.exists(image_path):
        print(f"⚠️ Image not found at {image_path}. Falling back to text only.")
        return send_text_message(f"⚠️ Screenshot missing. {message}")
    
    image_url = f"https://via.placeholder.com/800x400.png?text=Dummy+Test+Report"  # Replace this if you host real image

    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{message}*"}
        },
        {
            "type": "image",
            "title": {"type": "plain_text", "text": "Test Report Screenshot"},
            "image_url": image_url,
            "alt_text": "report"
        }
    ]

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
        json={"channel": SLACK_CHANNEL, "blocks": blocks}
    )

    if response.ok and response.json().get("ok"):
        print("✅ Slack image message sent.")
    else:
        print("❌ Slack image message failed:", response.text)

def send_text_message(message):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
        json={"channel": SLACK_CHANNEL, "text": message}
    )
    return response.ok

# 🎯 MAIN CALL
send_image_with_message(fallback_image_path, "📸 Automated Test Result Screenshot")
