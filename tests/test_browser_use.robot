*** Settings ***
Library           Process
Library           OperatingSystem

*** Test Cases ***
Browser Use Prompt Test
    [Documentation]    Run browser-use with a natural language prompt and check screenshot
    Run Process    python    slack_simulator.py
    Sleep    2s
    File Should Exist    screenshots/result.png
