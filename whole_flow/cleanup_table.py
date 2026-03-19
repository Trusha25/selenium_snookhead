import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import DEFAULT_TIMEOUT, GAME_NAME, TABLE_NAME
from utils.logger import setup_logger
from utils.helpers import click_js, save_screenshot
from pages.login_page import login


def open_setup_menu(driver, wait, logger):
    logger.info("Opening Set up menu")
    setup_menu = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Set up menu')]"))
    )
    click_js(driver, setup_menu)
    time.sleep(2)
    save_screenshot(driver, "cleanup_01_setup_menu", logger)


def open_game(driver, wait, game_name, logger):
    logger.info(f"Opening game: {game_name}")
    game = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//*[normalize-space()='{game_name}']"))
    )
    click_js(driver, game)
    time.sleep(2)
    save_screenshot(driver, "cleanup_02_game_opened", logger)


def enable_edit_mode(driver, wait, logger):
    logger.info("Enabling edit mode")

    edit_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'edit-mode-toggle') and normalize-space()='Edit']")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", edit_btn)

    time.sleep(2)
    save_screenshot(driver, "cleanup_03_edit_mode", logger)
    logger.info("Edit mode enabled")


def find_table_container(driver, table_name, logger):
    logger.info(f"Finding container for table: {table_name}")

    possible_xpaths = [
        f"//*[normalize-space()='{table_name}']/ancestor::div[contains(@class,'table-card')][1]",
        f"//*[normalize-space()='{table_name}']/ancestor::div[contains(@class,'setup')][1]",
        f"//*[normalize-space()='{table_name}']/ancestor::div[contains(@class,'card')][1]",
        f"//*[normalize-space()='{table_name}']/ancestor::tr[1]",
        f"//*[normalize-space()='{table_name}']/parent::div",
        f"//*[normalize-space()='{table_name}']/ancestor::div[1]",
    ]

    for xpath in possible_xpaths:
        try:
            container = driver.find_element(By.XPATH, xpath)
            logger.info(f"Found table container using xpath: {xpath}")
            return container
        except Exception:
            continue

    raise Exception(f"Could not find container for table '{table_name}'")


def click_delete_for_table(driver, wait, table_name, logger):
    logger.info(f"Trying to click delete for table: {table_name}")

    table_text = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[normalize-space()='{table_name}']"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", table_text)
    time.sleep(1)

    container = find_table_container(driver, table_name, logger)

    delete_candidates = [
        ".//button[@title='Delete Table']",
        ".//button[contains(@class,'delete')]",
        ".//*[name()='svg']/ancestor::button[1]",
        ".//button[.//*[name()='svg']]",
    ]

    for xpath in delete_candidates:
        try:
            delete_btn = container.find_element(By.XPATH, xpath)

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", delete_btn)
            time.sleep(1)

            try:
                wait.until(EC.element_to_be_clickable(delete_btn))
            except Exception:
                pass

            driver.execute_script("arguments[0].click();", delete_btn)
            logger.info(f"Clicked delete button using xpath: {xpath}")
            time.sleep(2)
            save_screenshot(driver, "cleanup_04_delete_button_clicked", logger)
            return
        except Exception as e:
            logger.info(f"Delete candidate failed: {xpath} | {e}")

    # fallback using full-page xpath relative to table name
    fallback_xpaths = [
        f"//*[normalize-space()='{table_name}']/following::button[@title='Delete Table'][1]",
        f"//*[normalize-space()='{table_name}']/following::button[contains(@class,'delete')][1]",
        f"//*[normalize-space()='{table_name}']/following::*[name()='svg'][1]/ancestor::button[1]",
    ]

    for xpath in fallback_xpaths:
        try:
            delete_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", delete_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", delete_btn)
            logger.info(f"Clicked delete button using fallback xpath: {xpath}")
            time.sleep(2)
            save_screenshot(driver, "cleanup_04_delete_button_clicked", logger)
            return
        except Exception as e:
            logger.info(f"Fallback delete xpath failed: {xpath} | {e}")

    raise Exception(f"Could not click delete button for table '{table_name}'")


def confirm_delete_popup(driver, logger):
    logger.info("Looking for delete confirmation popup")

    confirm_xpaths = [
        "//button[normalize-space()='Delete']",
        "//button[contains(text(),'Delete')]",
        "//button[normalize-space()='Confirm']",
        "//button[contains(text(),'Yes')]",
        "//button[contains(text(),'OK')]",
    ]

    for xpath in confirm_xpaths:
        try:
            confirm_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", confirm_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", confirm_btn)
            logger.info(f"Clicked popup confirmation using xpath: {xpath}")
            time.sleep(2)
            save_screenshot(driver, "cleanup_05_popup_delete_confirmed", logger)
            return
        except Exception:
            continue

    raise Exception("Delete confirmation popup appeared but no clickable confirm button was found")


def verify_table_deleted(driver, wait, table_name, logger):
    logger.info(f"Verifying deletion of table: {table_name}")

    time.sleep(3)

    try:
        wait.until_not(
            EC.presence_of_element_located((By.XPATH, f"//*[normalize-space()='{table_name}']"))
        )
        logger.info(f"Verified table deleted: {table_name}")
        save_screenshot(driver, "cleanup_06_delete_verified", logger)
        return True
    except TimeoutException:
        if table_name not in driver.page_source:
            logger.info(f"Verified table deleted from page source: {table_name}")
            save_screenshot(driver, "cleanup_06_delete_verified", logger)
            return True

        logger.error(f"Table still exists after delete attempt: {table_name}")
        save_screenshot(driver, "cleanup_06_delete_failed", logger)
        return False


def cleanup_table():
    logger = setup_logger()
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    try:
        logger.info("========== CLEANUP STARTED ==========")

        login(driver, wait, logger)
        open_setup_menu(driver, wait, logger)
        open_game(driver, wait, GAME_NAME, logger)
        enable_edit_mode(driver, wait, logger)

        click_delete_for_table(driver, wait, TABLE_NAME, logger)
        confirm_delete_popup(driver, logger)

        deleted = verify_table_deleted(driver, wait, TABLE_NAME, logger)
        assert deleted, f"Cleanup failed. Table '{TABLE_NAME}' was not deleted."

        logger.info("========== CLEANUP COMPLETED SUCCESSFULLY ==========")

    except Exception as e:
        logger.exception(f"Cleanup failed: {e}")
        raise

    finally:
        driver.quit()
        logger.info("Browser closed after cleanup")


if __name__ == "__main__":
    cleanup_table()