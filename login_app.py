# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import base64

EMAIL = os.environ.get('EASYHITS_EMAIL', 'piersilviogarrini+linadarini@gmail.com')
PASSWORD = os.environ.get('EASYHITS_PASSWORD', 'GF45!!dave')

print("Login Service Started")

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Opening home page...")
    driver.get("https://www.easyhits4u.com")
    time.sleep(3)
    
    print("Opening login page...")
    driver.get("https://www.easyhits4u.com/logon")
    time.sleep(3)
    
    # Salva screenshot della pagina login
    driver.save_screenshot("login_page.png")
    print("Screenshot saved: login_page.png")
    
    print("Waiting for login form to be ready...")
    wait = WebDriverWait(driver, 15)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = driver.find_element(By.NAME, "password")
    
    print("Entering credentials...")
    username_field.clear()
    username_field.send_keys(EMAIL)
    password_field.clear()
    password_field.send_keys(PASSWORD)
    
    print("Waiting for Enter button...")
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_green")))
    
    print("Submitting login...")
    driver.execute_script("arguments[0].click();", submit_button)
    
    # Attendi il redirect dopo il login
    time.sleep(8)
    
    # Stampa l'URL corrente per debug
    current_url = driver.current_url
    print("Current URL after login: {}".format(current_url))
    
    # Salva screenshot dopo il login
    driver.save_screenshot("after_login.png")
    print("Screenshot saved: after_login.png")
    
    # Controlla se c'è un errore nella pagina
    page_text = driver.find_element(By.TAG_NAME, "body").text
    if "warning=il" in current_url or "Invalid" in page_text:
        print("Login failed: invalid credentials or Turnstile")
    elif "account/home" in current_url or "surf" in current_url:
        print("Login successful!")
    else:
        print("Unknown status, check screenshots")
    
    # Ottieni tutti i cookie
    cookies = driver.get_cookies()
    print("Number of cookies found: {}".format(len(cookies)))
    
    user_id = None
    sesids = None
    
    for cookie in cookies:
        print("Cookie: {} = {}".format(cookie['name'], cookie['value'][:30] if len(cookie['value']) > 30 else cookie['value']))
        if cookie['name'] == 'user_id':
            user_id = cookie['value']
        if cookie['name'] == 'sesids':
            sesids = cookie['value']
    
    print("=" * 60)
    print("COOKIE STRING:")
    if user_id and sesids:
        print("user_id={}; sesids={}".format(user_id, sesids))
    else:
        print("No valid cookies found")
    print("=" * 60)
    
except Exception as e:
    print("ERROR: {}".format(e))
    driver.save_screenshot("error.png")
    print("Screenshot saved: error.png")
finally:
    driver.quit()