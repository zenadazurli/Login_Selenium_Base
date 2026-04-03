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
    # 1. Vai alla home (per i cookie iniziali)
    print("Opening home page...")
    driver.get("https://www.easyhits4u.com")
    time.sleep(3)
    
    # 2. Vai direttamente alla pagina di login (per avere il form pulito)
    print("Opening login page...")
    driver.get("https://www.easyhits4u.com/logon")
    time.sleep(5)  # Aspetta che tutto il JavaScript sia eseguito
    
    # 3. Cerca eventuali token CSRF (esempio: name="csrf_token")
    csrf_token = None
    try:
        csrf_element = driver.find_element(By.NAME, "csrf_token")
        csrf_token = csrf_element.get_attribute("value")
        print("CSRF Token found: {}".format(csrf_token))
    except:
        print("No CSRF token found, proceeding without it")
    
    # 4. Inserisci le credenziali
    print("Entering credentials...")
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    
    username_field.clear()
    username_field.send_keys(EMAIL)
    password_field.clear()
    password_field.send_keys(PASSWORD)
    
    # 5. Invia il modulo
    print("Submitting login...")
    
    # Opzione A: Se c'è un pulsante "Enter", usalo
    try:
        submit_button = driver.find_element(By.CSS_SELECTOR, "button.btn_green")
        driver.execute_script("arguments[0].click();", submit_button)
    except:
        # Opzione B: Altrimenti, invia il modulo direttamente
        form = driver.find_element(By.TAG_NAME, "form")
        driver.execute_script("arguments[0].submit();", form)
    
    # 6. Attendi il reindirizzamento
    time.sleep(8)
    print("Current URL: {}".format(driver.current_url))
    
    # 7. Verifica il successo
    if "warning=il" in driver.current_url:
        print("LOGIN FAILED: Invalid credentials or missing CSRF token")
    else:
        print("LOGIN SUCCESSFUL!")
        
        # Vai alla pagina di surf per generare i cookie finali
        driver.get("https://www.easyhits4u.com/surf/?surftype=2&q=start")
        time.sleep(5)
        
        cookies = driver.get_cookies()
        user_id = next((c['value'] for c in cookies if c['name'] == 'user_id'), None)
        sesids = next((c['value'] for c in cookies if c['name'] == 'sesids'), None)
        
        if user_id and sesids:
            print("COOKIE STRING: user_id={}; sesids={}".format(user_id, sesids))
        else:
            print("No user cookies found after navigation")
    
except Exception as e:
    print("ERROR: {}".format(e))
finally:
    driver.quit()