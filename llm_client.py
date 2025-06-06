# llm_client.py

def get_test_steps(prompt):
    print(f"Gemini Prompt Received: {prompt}")
    return [
        {"action": "goto", "url": "https://example.com"},
        {"action": "click", "selector": "text=Login"},
        {"action": "fill", "selector": "input[name='username']", "value": "admin"},
        {"action": "fill", "selector": "input[name='password']", "value": "password"},
        {"action": "click", "selector": "text=Submit"},
    ]
