from playwright.sync_api import sync_playwright
import time
from twilio.rest import Client

account_sid = 'YOUR_TWILIO_SID'
auth_token = 'YOUR_TWILIO_TOKEN'
client = Client(account_sid, auth_token)

FROM = '+1xxxxxxxxx' 
TO = '+9xxxxxxxxxx'  

#Replace with match url : dont forget to update match url
CRICBUZZ_URL = 'https://www.cricbuzz.com/live-cricket-scores/115230'

last_six_ball = ""

def send_message(message):
    msg = client.messages.create(body=message, from_=FROM, to=TO)
    print(msg.sid)
    print("6 runs hit:", message)

def check_for_six(page):
    global last_sent
    page.goto(CRICBUZZ_URL, timeout=60000)
    page.wait_for_load_state('networkidle', timeout=15000)


    # Grab all commentary lines
    six_lines = page.query_selector_all('p.cb-com-ln')[:1] 

    for p in six_lines:
        text = p.inner_text().strip()
        if "six" in text.lower() and text != last_sent:
            last_sent = text
            text = "A six has been hit, you can order now at swiggy" + text;
            return text
        else:
            last_sent = text
    return None

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    while True:
        msg = check_for_six(page)
        if msg:
            send_message(msg)
            time.sleep(30)
        else:
            time.sleep(30)

    