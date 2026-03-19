import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from config import DEFAULT_TIMEOUT, TABLE_NAME, GAME_NAME, MEMBER_NAME
from utils.logger import setup_logger

from pages.login_page import login
from pages.owner_panel_page import open_owners_panel, get_revenue
from pages.setup_page import open_setup_menu, open_game, create_table
from pages.dashboard_page import go_to_dashboard, book_table, wait_for_timer
from pages.billing_page import open_billing_page, pay_bill_for_member

def run_test():
    logger = setup_logger()
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    try:
        logger.info("=== Test started ===")

        login(driver, wait, logger)

        open_owners_panel(driver, wait, logger)
        initial_revenue = get_revenue(wait)
        logger.info(f"Initial revenue: {initial_revenue}")

        open_setup_menu(driver, wait, logger)
        open_game(driver, wait, GAME_NAME, logger)
        create_table(driver, wait, TABLE_NAME, logger)

        go_to_dashboard(driver, wait, logger)
        book_table(driver, wait, GAME_NAME, TABLE_NAME, MEMBER_NAME, logger)

        wait_for_timer(driver, 70, logger)

        open_billing_page(driver, wait, logger)
        paid_amount = pay_bill_for_member(driver, wait, MEMBER_NAME, logger)

        open_owners_panel(driver, wait, logger)
        updated_revenue = get_revenue(wait)
        logger.info(f"Updated revenue: {updated_revenue}")

        assert updated_revenue >= initial_revenue, "Revenue did not increase."
        assert (
            updated_revenue >= initial_revenue + paid_amount
            or updated_revenue > initial_revenue
        ), "Revenue update seems incorrect."

        logger.info("=== Test passed successfully ===")

    except Exception as e:
        logger.exception(f"Test failed: {e}")
        raise

    finally:
        driver.quit()
        logger.info("Browser closed")

if __name__ == "__main__":
    run_test()