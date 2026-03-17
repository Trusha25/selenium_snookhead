from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# This script automates fixed-time table booking in the Snookhead web app.
# It logs in, selects a table, enters customer/member details,
# sets a specific booking time (e.g., 10 minutes), confirms the booking,
# handles popups, waits for the timer to run, and captures screenshots.

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
table_b = wait.until(
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
customer = wait.until(
    EC.presence_of_element_located((By.XPATH,  "//input[@placeholder='Search member or enter name...']"))
)
customer.clear()
customer.send_keys("b")
time.sleep(2)

# ---------- SELECT DEFAULT MEMBER ----------
member = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'battata_wada')]"))
)
driver.execute_script("arguments[0].click();", member)

print("Member selected")
time.sleep(1)
ss(driver, "03_member_selected")

# ---------- ENTER TIME = 10 ----------
time_box = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
)
time_box.clear()
time_box.send_keys("1")

print("Time set to 10 mins")
time.sleep(1)
ss(driver, "04_time_entered")

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
time.sleep(100)

ss(driver, "07_timer_check")

# ---------- CLOSE ----------
driver.quit()
print("Test completed")