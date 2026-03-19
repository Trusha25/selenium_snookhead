from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, EMAIL, PASSWORD
from utils.helpers import save_screenshot

def login(driver, wait, logger):
    driver.get(BASE_URL)
    logger.info("Opened application")

    email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    password = driver.find_element(By.XPATH, "//input[@type='password']")

    email.send_keys(EMAIL)
    password.send_keys(PASSWORD)

    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]")))
    logger.info("Login successful")
    save_screenshot(driver, "01_dashboard", logger)