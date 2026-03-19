import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import click_js, save_screenshot, click_ok_popup

def go_to_dashboard(driver, wait, logger):
    dashboard = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Dashboard')]"))
    )
    click_js(driver, dashboard)
    time.sleep(2)
    save_screenshot(driver, "07_dashboard_again", logger)
    logger.info("Returned to Dashboard")

def book_table(driver, wait, game_name, table_name, member_name, logger):
    try:
        game = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(),'{game_name}')]"))
        )
        click_js(driver, game)
        time.sleep(2)
    except TimeoutException:
        logger.info(f"{game_name} card not clicked again, continuing")

    table_card = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//div[contains(@class,'table-card') and .//*[contains(text(),'{table_name}')]]"
        ))
    )
    click_js(driver, table_card)
    time.sleep(2)
    save_screenshot(driver, "08_table_opened", logger)

    customer = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//label[text()='Customer Name']/following::input[1]"
        ))
    )
    customer.clear()
    customer.send_keys("b")
    time.sleep(2)

    member = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(),'{member_name}')]"))
    )
    click_js(driver, member)

    time_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
    )
    time_input.clear()
    time_input.send_keys("1")

    save_screenshot(driver, "09_booking_details_filled", logger)

    confirm_booking = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class,'book-btn-unified') or contains(text(),'Confirm Booking')]"
        ))
    )
    click_js(driver, confirm_booking)
    time.sleep(2)
    save_screenshot(driver, "10_booking_confirmed", logger)
    logger.info("Table booked successfully")

    click_ok_popup(driver, logger)

def wait_for_timer(driver, seconds, logger):
    logger.info(f"Waiting for {seconds} seconds for timer to complete")
    time.sleep(seconds)
    click_ok_popup(driver, logger)
    save_screenshot(driver, "timer_completed_popup", logger)