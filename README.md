# PowerLynx Wi-Fi Brute Forcer

This script uses PyAutoGUI to navigate the Windows Wi-Fi menu, and Selenium to brute-force a captive portal login page. 

## Requirements
- Python 3.x
- Google Chrome installed
- Libraries: `pyautogui`, `pyperclip`, `selenium`

## Setup
1. Run `pip install pyautogui pyperclip selenium`
2. Update the coordinates at the top of `brute.py` to match your screen resolution.
3. The `my_passwords.txt` file is included. 
4. Run `py brute.py`