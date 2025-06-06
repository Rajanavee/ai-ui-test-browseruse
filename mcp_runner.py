from llm_client import get_test_steps
from playwright.sync_api import sync_playwright

def run_ai_test(prompt):
    steps = get_test_steps(prompt)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for step in steps:
            action = step['action']
            if action == "goto":
                page.goto(step['url'])
            elif action == "click":
                page.click(step['selector'])
            elif action == "fill":
                page.fill(step['selector'], step['value'])

        page.screenshot(path="screenshots/final.png")
        browser.close()

if __name__ == "__main__":
    run_ai_test("Login to example.com and verify dashboard")
