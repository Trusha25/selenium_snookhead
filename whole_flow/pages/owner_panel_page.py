import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import OWNER_PASSWORD
from utils.helpers import click_js, get_text, parse_amount, save_screenshot

def open_owners_panel(driver, wait, logger):
    owners_panel = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),\"Owners panel\")]"))
    )
    click_js(driver, owners_panel)

    password_box = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//input[@type='password' or contains(@placeholder,'password') or contains(@placeholder,'Password')]"
        ))
    )
    password_box.clear()
    password_box.send_keys(OWNER_PASSWORD)

    access_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Access')]"))
    )
    click_js(driver, access_btn)

    time.sleep(3)
    save_screenshot(driver, "02_owners_panel", logger)
    logger.info("Opened Owner's Panel")

def get_revenue(wait):
    revenue_text = get_text(wait, "//*[contains(text(),'Revenue')]/following::*[1]")
    return parse_amount(revenue_text)