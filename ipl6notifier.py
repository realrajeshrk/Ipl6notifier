from playwright.sync_api 
import sync_playwright
import time


FROM = 'whatsapp:+14155238886' 
TO = 'whatsapp:+91YOURNUMBER'  

CRICBUZZ_URL = 'https://www.cricbuzz.com/live-cricket-scores/115230/rcb-vs-rr-42nd-match-indian-premier-league-2025'

last_six_ball = ""

def send_message(message):
    # client.messages.create(body=message, from_=FROM, to=TO)
    # message logic need to implement
    print("6 runs hit:", message)

def check_for_six(page):
    global last_sent
    page.goto(CRICBUZZ_URL, timeout=60000)
    page.wait_for_load_state('networkidle', timeout=15000)


    # Grab all commentary lines
    six_lines = page.query_selector_all('p.cb-com-ln')[:1] 

    for p in six_lines:
        text = p.inner_text().strip()
        print(text);
        if "six" in text.lower() and text != last_sent:
            last_sent = text
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
            print("Not a 6 run")
            time.sleep(30)

    