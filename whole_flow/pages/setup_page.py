import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import click_js, save_screenshot

def open_setup_menu(driver, wait, logger):
    setup_menu = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Set up menu')]"))
    )
    click_js(driver, setup_menu)
    time.sleep(2)
    save_screenshot(driver, "03_setup_menu", logger)
    logger.info("Opened Set up menu")

def open_game(driver, wait, game_name, logger):
    game = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//*[normalize-space()='{game_name}']"))
    )
    click_js(driver, game)
    time.sleep(2)
    save_screenshot(driver, "04_game_opened", logger)
    logger.info(f"Opened {game_name}")

def create_table(driver, wait, table_name, logger):
    add_tables_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add New Table')]"))
    )
    click_js(driver, add_tables_btn)
    time.sleep(2)

    table_name_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Table')]"))
    )
    table_name_input.clear()
    table_name_input.send_keys(table_name)

    type_box = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Standard')]"))
    )
    type_box.clear()
    type_box.send_keys("Standard")

    nums = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@type='number']"))
    )

    values = ["10", "300", "600", "50"]
    for i, val in enumerate(values):
        nums[i].clear()
        nums[i].send_keys(val)

    save_screenshot(driver, "05_table_details_filled", logger)

    create_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create')]"))
    )
    click_js(driver, create_btn)
    time.sleep(2)

    created_table = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{table_name}')]"))
    )
    assert created_table.is_displayed(), "Table creation failed."

    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]")))
    time.sleep(2)

    save_screenshot(driver, "06_table_created", logger)
    logger.info(f"Created table: {table_name}")