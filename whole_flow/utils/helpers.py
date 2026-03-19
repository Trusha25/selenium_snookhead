import os
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import SCREENSHOT_DIR

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def save_screenshot(driver, name, logger=None):
    path = f"{SCREENSHOT_DIR}/{name}.png"
    driver.save_screenshot(path)
    if logger:
        logger.info(f"Screenshot saved: {path}")

def click_js(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", element)

def parse_amount(text):
    cleaned = re.sub(r"[^\d.]", "", text)
    return float(cleaned) if cleaned else 0.0

def get_text(wait, xpath):
    return wait.until(
        EC.presence_of_element_located((By.XPATH, xpath))
    ).text.strip()

def click_ok_popup(driver, logger=None):
    try:
        ok_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(text(),'OK') or contains(text(),'Ok')]"
            ))
        )
        driver.execute_script("arguments[0].click();", ok_btn)
        if logger:
            logger.info("OK popup handled")
        time.sleep(2)
    except Exception:
        if logger:
            logger.info("Popup not present")