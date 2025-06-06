# # import subprocess
# # import os
# # import shutil
# # from pathlib import Path

# # def run_browser_use(prompt: str):
# #     print(f"📥 Prompt received: {prompt}")
    
# #     # Correct CLI usage with --prompt
# #     subprocess.run(["browser-use", "--prompt", prompt])

# #     # Copy latest screenshot
# #     home = str(Path.home())
# #     screenshot_dir = os.path.join(home, ".browseruse", "screenshots")
# #     os.makedirs("screenshots", exist_ok=True)

# #     try:
# #         files = sorted(Path(screenshot_dir).glob("*.png"), key=os.path.getmtime)
# #         latest = str(files[-1])
# #         dst = os.path.join("screenshots", "result.png")
# #         shutil.copy(latest, dst)
# #         print(f"✅ Screenshot saved to {dst}")
# #     except Exception as e:
# #         print("⚠️ Error saving screenshot:", e)

# # # Simulate Slack prompt
# # prompt = "Go to https://example.com and take a screenshot"
# # print("🟢 Simulating Slack Prompt ➤", prompt)
# # run_browser_use(prompt)


# # from browser_use_runner import run_browser_use


# # prompt = "Open https://example.com, wait for the page to load fully, take a full-screen screenshot and save it to disk"
# # print("🟢 Simulating Slack Prompt ➤", prompt)

# # success = run_browser_use(prompt)

# # if success:
# #     print("🎯 Test execution and screenshot done!")
# # else:
# #     print("❌ Something went wrong")

# import os
# import requests
# from PIL import Image
# from dotenv import load_dotenv

# load_dotenv()

# SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#ai-results")

# def merge_screenshots(input_folder, output_path):
#     files = sorted([f for f in os.listdir(input_folder) if f.endswith(".png")])
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
#     # Upload image
#     with open(image_path, "rb") as f:
#         response = requests.post(
#             "https://slack.com/api/files.upload",
#             headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
#             files={"file": f},
#             data={
#                 "channels": SLACK_CHANNEL,
#                 "initial_comment": text + (f"\n📎 [Report]({report_url})" if report_url else "")
#             }
#         )

#     if response.status_code == 200 and response.json().get("ok"):
#         print("✅ Report sent to Slack.")
#     else:
#         print("❌ Failed to send Slack message:", response.text)

# if __name__ == "__main__":
#     image = merge_screenshots("screenshots", "screenshots/combined.png")

#     # Check test result from robot output
#     status = "✅ PASS" if os.path.exists("screenshots/result.png") else "❌ FAIL"
#     send_to_slack(
#         text=f"{status} - AI UI Test Result",
#         image_path=image,
#         report_url="(attach Jenkins report URL here)"
#     )
import os
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#ai-results")

def merge_screenshots(input_folder, output_path):
    if not os.path.exists(input_folder):
        print("⚠️ Folder not found: screenshots. Using fallback image.")
        return "fallback.png"

    files = sorted([f for f in os.listdir(input_folder) if f.endswith(".png")])
    if not files:
        print("⚠️ No screenshots found. Using fallback image.")
        return "fallback.png"

    images = [Image.open(os.path.join(input_folder, f)) for f in files]
    widths, heights = zip(*(img.size for img in images))
    total_height = sum(heights)
    max_width = max(widths)

    combined = Image.new("RGB", (max_width, total_height))
    y_offset = 0
    for img in images:
        combined.paste(img, (0, y_offset))
        y_offset += img.size[1]

    combined.save(output_path)
    print(f"✅ Combined screenshot saved to {output_path}")
    return output_path

def send_to_slack(text, image_path, report_url=None):
    # Upload the image file to Slack to get a public URL
    with open(image_path, "rb") as f:
        response = requests.post(
            "https://slack.com/api/files.upload",
            headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
            files={"file": f},
            data={"channels": SLACK_CHANNEL}
        )

    if response.status_code != 200 or not response.json().get("ok"):
        print("❌ Failed to upload image:", response.text)
        return

    file_info = response.json()["file"]
    image_url = file_info["url_private"]

    # Send a message with image link
    message = f"{text}\n🖼 Image: {image_url}"
    if report_url:
        message += f"\n📎 [Report]({report_url})"

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "channel": SLACK_CHANNEL,
            "text": message
        }
    )

    if response.status_code == 200 and response.json().get("ok"):
        print("✅ Report sent to Slack.")
    else:
        print("❌ Failed to send Slack message:", response.text)

if __name__ == "__main__":
    image = merge_screenshots("screenshots", "screenshots/combined.png")

    status = "✅ PASS" if os.path.exists("screenshots/result.png") else "❌ FAIL"
    send_to_slack(
        text=f"{status} - AI UI Test Result",
        image_path=image,
        report_url="https://jenkins.example.com/job/AI_UI_Test_Bot/lastBuild"
    )
