# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

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
    print("1. Opening home page...")
    driver.get("https://www.easyhits4u.com")
    time.sleep(3)
    print("   URL: {}".format(driver.current_url))
    
    print("2. Opening login page...")
    driver.get("https://www.easyhits4u.com/logon")
    time.sleep(3)
    print("   URL: {}".format(driver.current_url))
    
    print("3. Waiting for login form...")
    wait = WebDriverWait(driver, 15)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = driver.find_element(By.NAME, "password")
    
    print("4. Entering credentials...")
    username_field.clear()
    username_field.send_keys(EMAIL)
    password_field.clear()
    password_field.send_keys(PASSWORD)
    
    print("5. Clicking Enter button...")
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_green")))
    driver.execute_script("arguments[0].click();", submit_button)
    
    # Controlla l'URL dopo 3 secondi
    time.sleep(3)
    url_after_click = driver.current_url
    print("6. URL after 3 seconds: {}".format(url_after_click))
    
    # Controlla l'URL dopo 8 secondi
    time.sleep(5)
    url_after_wait = driver.current_url
    print("7. URL after 8 seconds: {}".format(url_after_wait))
    
    # Controlla se c'è warning=il (login fallito)
    if "warning=il" in url_after_wait:
        print("   -> LOGIN FAILED: invalid credentials or Turnstile")
    elif "account/home" in url_after_wait:
        print("   -> LOGIN SUCCESS: redirect to account/home")
    elif "surf" in url_after_wait:
        print("   -> LOGIN SUCCESS: already on surf page")
    else:
        print("   -> UNKNOWN: {}".format(url_after_wait))
    
    # Prova a navigare alla surf page
    print("8. Navigating to surf page...")
    driver.get("https://www.easyhits4u.com/surf/?surftype=2&q=start")
    time.sleep(3)
    print("   URL after surf: {}".format(driver.current_url))
    
    # Cookie
    cookies = driver.get_cookies()
    print("\n9. COOKIES FOUND: {}".format(len(cookies)))
    for cookie in cookies:
        if cookie['name'] in ['user_id', 'sesids', '_cfuvid']:
            print("   {} = {}".format(cookie['name'], cookie['value'][:30] if len(cookie['value']) > 30 else cookie['value']))
    
    user_id = next((c['value'] for c in cookies if c['name'] == 'user_id'), None)
    sesids = next((c['value'] for c in cookies if c['name'] == 'sesids'), None)
    
    print("\n" + "=" * 60)
    if user_id and sesids:
        print("SUCCESS!")
        print("user_id={}; sesids={}".format(user_id, sesids))
    else:
        print("FAILED: No cookies")
    print("=" * 60)
    
except Exception as e:
    print("ERROR: {}".format(e))
finally:
    driver.quit()