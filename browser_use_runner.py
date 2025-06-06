# import os
# from browser_use import run_prompt

# def run_browser_use(prompt: str):
#     print(f"📥 Prompt received: {prompt}")
#     result = run_prompt(prompt)

#     # Optional: Copy screenshot from /tmp to screenshots/ folder
#     os.makedirs("screenshots", exist_ok=True)

#     if isinstance(result, dict) and "screenshot_path" in result:
#         src = result["screenshot_path"]
#         dst = os.path.join("screenshots", "result.png")
#         try:
#             os.system(f"cp {src} {dst}")
#             print(f"✅ Screenshot saved to {dst}")
#         except Exception as e:
#             print("⚠️ Error saving screenshot:", e)
#     else:
#         print("⚠️ Screenshot path not returned in result")

#     return result


import os
from playwright.sync_api import sync_playwright

def run_browser_use(prompt: str = ""):
    print("📥 Running manual browser script (ignoring prompt)...")

    # Ensure screenshot folder exists
    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto("https://example.com", timeout=60000)
        page.wait_for_load_state("networkidle")

        screenshot_path = "screenshots/result.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"✅ Screenshot saved to {screenshot_path}")

        browser.close()
        return True
