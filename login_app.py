# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time

EMAIL = os.environ.get('EASYHITS_EMAIL', 'piersilviogarrini+linadarini@gmail.com')
PASSWORD = os.environ.get('EASYHITS_PASSWORD', 'GF45!!dave')

print("Login Service Started")

# Configura Chrome
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
    
    print("Entering credentials...")
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    
    username_field.send_keys(EMAIL)
    password_field.send_keys(PASSWORD)
    
    print("Submitting login...")
    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    submit_button.click()
    
    time.sleep(5)
    
    # Ottieni cookie
    cookies = driver.get_cookies()
    user_id = None
    sesids = None
    
    for cookie in cookies:
        if cookie['name'] == 'user_id':
            user_id = cookie['value']
        if cookie['name'] == 'sesids':
            sesids = cookie['value']
    
    print("=" * 60)
    print("COOKIE STRING:")
    print("user_id={}; sesids={}".format(user_id, sesids))
    print("=" * 60)
    
except Exception as e:
    print("ERROR: {}".format(e))
finally:
    driver.quit()