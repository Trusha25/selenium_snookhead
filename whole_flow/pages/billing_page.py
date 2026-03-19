import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import click_js, save_screenshot, parse_amount

def open_billing_page(driver, wait, logger):
    billing = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Billing')]"))
    )
    click_js(driver, billing)
    time.sleep(2)
    save_screenshot(driver, "11_billing_page", logger)
    logger.info("Opened Billing page")

def pay_bill_for_member(driver, wait, member_name, logger):
    bill_row = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{member_name}')]"))
    )
    assert bill_row.is_displayed(), f"Bill for {member_name} not found."

    pay_bill_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class,'view-bill-btn') and normalize-space()='Pay Now']"
        ))
    )

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pay_bill_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", pay_bill_btn)

    time.sleep(2)
    save_screenshot(driver, "12_pay_bill_clicked", logger)

    pay_amount_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class,'pay-btn') and contains(text(),'Pay')]"
        ))
    )
    paid_amount = parse_amount(pay_amount_btn.text.strip())

    click_js(driver, pay_amount_btn)
    time.sleep(2)
    save_screenshot(driver, "13_payment_done", logger)
    logger.info(f"Paid bill amount: {paid_amount}")

    return paid_amount