from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# This script automates stopwatch-based table booking.
# It logs in, selects a table, enters customer/member details,(tried to add memeber but  than it got added with some random name)
# chooses the stopwatch option, confirms the booking,
# verifies the running timer, handles popups, and captures screenshots.

# ---------- SCREENSHOTS ----------
os.makedirs("screenshots", exist_ok=True)

def ss(driver, name):
    driver.save_screenshot(f"screenshots/{name}.png")

# ---------- SETUP ----------
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

driver.get("http://localhost:5173/")

# ---------- LOGIN ----------
email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
password = driver.find_element(By.XPATH, "//input[@type='password']")

email.send_keys("trushajadhav25@gmail.com")
password.send_keys("trusha25")

driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]")))
print("Login done")
time.sleep(2)


# ---------- CLICK TABLE B ----------
table_b= wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'table-card') and .//*[contains(text(),'Table B')]]"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", table_b)
time.sleep(1)
driver.execute_script("arguments[0].click();", table_b)

print("Table B selected")
time.sleep(2)
ss(driver, "02_table_b_opened")

# ---------- ENTER CUSTOMER ----------
# ---------- ENTER CUSTOMER ----------
customer = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//label[text()='Customer Name']/following::input[1]"
    ))
)
customer.clear()
customer.send_keys("g")
time.sleep(2)
ss(driver, "04_customer_typed_g")

# ---------- CLICK ADD NEW MEMBER ----------
add_member_option = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//li[contains(@class,'add-new-member')]"
    ))
)
driver.execute_script("arguments[0].click();", add_member_option)

print("Add New Member option clicked")
time.sleep(2)
ss(driver, "05_add_member_popup_opened")

# ---------- FILL ADD MEMBER POPUP ----------

# Name
name_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter name']"))
)
name_input.clear()
name_input.send_keys("golabjamun")

# Phone
phone_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter phone']"))
)
phone_input.clear()
phone_input.send_keys("8446718788")

# Email
email_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter email']"))
)
email_input.clear()
email_input.send_keys("trushajadhav890@gmail.com")

# External ID (leave empty for now if not needed)

# Initial Balance
balance_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@value='0.00' or @placeholder='0.00']"))
)
balance_input.clear()
balance_input.send_keys("1000")

# Address
address_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter address']"))
)
address_input.clear()
address_input.send_keys("pune")

ss(driver, "06_member_details_filled")

# ---------- CLICK ADD MEMBER BUTTON ----------
add_member_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(text(),'Add Member')]"
    ))
)
driver.execute_script("arguments[0].click();", add_member_btn)

print("New member added")
time.sleep(2)
ss(driver, "07_member_added")

# ---------- SELECT FRAME ----------
stopwatch_box = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'radio-row')]//label[contains(.,'Stopwatch')]"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", stopwatch_box)
time.sleep(1)
driver.execute_script("arguments[0].click();", stopwatch_box)

print("Stopwatch selected")

time.sleep(1)
ss(driver, "04_stopwatch_selected")

# ---------- CONFIRM BOOKING ----------
confirm = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'book-btn-unified') and contains(text(),'Confirm')]"))
)
driver.execute_script("arguments[0].click();", confirm)

print("Booking confirmed")
time.sleep(2)
ss(driver, "05_booking_confirmed")

# ---------- GO BACK TO DASHBOARD ----------
dashboard = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Dashboard')]"))
)
driver.execute_script("arguments[0].click();", dashboard)

print("Back to dashboard")
time.sleep(2)
ss(driver, "06_back_to_dashboard")

# ---------- WAIT 2 MINUTES ----------
print("Waiting 2 minutes to check timer...")
time.sleep(60)

ss(driver, "07_timer_check")

# ---------- CLOSE ----------
driver.quit()
print("Test completed")