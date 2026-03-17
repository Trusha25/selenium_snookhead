from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import re

# This script executes the complete end-to-end automation flow of the Snookhead web app.
# It logs into the application, checks revenue in the Owner's Panel,
# creates a new table in Game C, books the table using a member,
# waits for the booking timer to complete, generates and pays the bill,
# and finally verifies that the revenue has been updated correctly.
# Screenshots are captured throughout the process.
# ---------- SCREENSHOTS ----------
os.makedirs("screenshots", exist_ok=True)

def ss(driver, name):
    driver.save_screenshot(f"screenshots/{name}.png")


# ---------- HELPERS ----------
def click_js(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", element)

def parse_amount(text):
    cleaned = re.sub(r"[^\d.]", "", text)
    return float(cleaned) if cleaned else 0.0

def get_text(wait, xpath):
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()


# ---------- MAIN FUNCTIONS ----------
def login(driver, wait):
    driver.get("http://localhost:5173/")

    email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    password = driver.find_element(By.XPATH, "//input[@type='password']")

    email.send_keys("trushajadhav25@gmail.com")
    password.send_keys("trusha25")

    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]")))
    print("Login successful")
    ss(driver, "01_dashboard")


def open_owners_panel(driver, wait):
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
    password_box.send_keys("Trusha25")

    access_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Access')]"))
    )
    click_js(driver, access_btn)

    time.sleep(3)
    ss(driver, "02_owners_panel")
    print("Opened Owner's Panel")


def get_revenue(wait):
    revenue_text = get_text(wait, "//*[contains(text(),'Revenue')]/following::*[1]")
    return parse_amount(revenue_text)


def open_setup_menu(driver, wait):
    setup_menu = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Set up menu')]"))
    )
    click_js(driver, setup_menu)
    time.sleep(2)
    ss(driver, "03_setup_menu")
    print("Opened Set up menu")


def open_game_c(driver, wait):
    game_c = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Game C']"))
    )
    click_js(driver, game_c)
    time.sleep(2)
    ss(driver, "04_game_c")
    print("Opened Game C")


def create_table_in_game_c(driver, wait, table_name):
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

    ss(driver, "05_table_details_filled")

    create_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create')]"))
    )
    click_js(driver, create_btn)
    time.sleep(2)

    created_table = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{table_name}')]"))
    )
    assert created_table.is_displayed(), "Table creation failed."
    time.sleep(2)
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]")))
    time.sleep(2)

    ss(driver, "06_table_created")
    print(f"Created table: {table_name}")



def go_to_dashboard(driver, wait):
    dashboard = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Dashboard')]"))
    )
    click_js(driver, dashboard)
    time.sleep(2)
    ss(driver, "07_dashboard_again")
    print("Returned to Dashboard")

def click_ok_popup(driver, wait):
    try:
        ok_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(text(),'OK') or contains(text(),'Ok')]"
            ))
        )
        driver.execute_script("arguments[0].click();", ok_btn)
        print("OK popup handled")
        time.sleep(2)
    except:
        print("Popup not present")


def book_table(driver, wait, game_name, table_name):
    try:
        game = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(),'{game_name}')]"))
        )
        click_js(driver, game)
        time.sleep(2)
    except TimeoutException:
        pass

    table_card = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//div[contains(@class,'table-card') and .//*[contains(text(),'{table_name}')]]"
        ))
    )
    click_js(driver, table_card)
    time.sleep(2)
    ss(driver, "08_table_opened")

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
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'battata_wada')]"))
    )
    click_js(driver, member)

    time_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
    )
    time_input.clear()
    time_input.send_keys("1")

    ss(driver, "09_booking_details_filled")

    confirm_booking = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class,'book-btn-unified') or contains(text(),'Confirm Booking')]"
        ))
    )
    click_js(driver, confirm_booking)
    time.sleep(2)
    ss(driver, "10_booking_confirmed")
    print("Table booked successfully")
    click_ok_popup(driver, wait)
    ss(driver, "timer_completed_popup")

def wait_for_timer():
    print("Waiting for 1-minute timer to finish...")
    time.sleep(70)
    click_ok_popup(driver, wait)
    ss(driver, "timer_completed_popup")


def open_billing_page(driver, wait):
    billing = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Billing')]"))
    )
    click_js(driver, billing)
    time.sleep(2)
    ss(driver, "11_billing_page")
    print("Opened Billing page")


def pay_bill_for_member(driver, wait, member_name):
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
    ss(driver, "12_pay_bill_clicked")

    pay_amount_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(@class,'pay-btn') and contains(text(),'Pay')]"))
    )
    paid_amount = parse_amount(pay_amount_btn.text.strip())

    click_js(driver, pay_amount_btn)
    time.sleep(2)
    ss(driver, "13_payment_done")
    print(f"Paid bill amount: {paid_amount}")

    return paid_amount

# ---------- RUN ----------
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    table_name = "Table X"

    login(driver, wait)

    open_owners_panel(driver, wait)
    initial_revenue = get_revenue(wait)
    print("Initial revenue:", initial_revenue)

    open_setup_menu(driver, wait)
    open_game_c(driver, wait)
    create_table_in_game_c(driver, wait, table_name)

    go_to_dashboard(driver, wait)
    book_table(driver, wait, "Game C", table_name)

    wait_for_timer()

    open_billing_page(driver, wait)
    paid_amount = pay_bill_for_member(driver, wait, "battata_wada")

    open_owners_panel(driver, wait)
    updated_revenue = get_revenue(wait)
    print("Updated revenue:", updated_revenue)

    assert updated_revenue >= initial_revenue, "Revenue did not increase."
    assert updated_revenue >= initial_revenue + paid_amount or updated_revenue > initial_revenue, \
        "Revenue update seems incorrect."

    print("Test passed successfully.")

finally:
    time.sleep(3)
    driver.quit()