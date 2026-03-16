from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Summary:
# This script automates the creation of tables for Game A in the Snookhead
# web application. It logs into the system, opens Game A, and creates
# multiple tables with predefined types and pricing values while capturing screenshots.



# ---------- Screenshot Folder ----------
os.makedirs("screenshots", exist_ok=True)

def screenshot(driver, name):
    driver.save_screenshot(f"screenshots/{name}.png")


# ---------- TABLE DATA ----------
tables = [
    ("Table A", "Standard"),
    ("Table B", "Standard"),
    ("Table C", "Premium")
]

prices = {
    "Standard": (15, 320, 650, 55),
    "Premium": (25, 450, 900, 75)
}


# ---------- BROWSER ----------
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

driver.get("http://localhost:5173/")


# ---------- LOGIN ----------
email = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
)

password = driver.find_element(By.XPATH, "//input[@type='password']")

email.send_keys("trushajadhav25@gmail.com")
password.send_keys("a7b3SNuSUrYyDUx")

driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

wait.until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]"))
)

screenshot(driver, "01_dashboard")

print("Login successful")


# ---------- CLICK ADD TABLES ----------
add_tables_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Tables')]"))
)

driver.execute_script("arguments[0].click();", add_tables_btn)

time.sleep(2)
screenshot(driver, "02_add_tables_clicked")

print("Add Tables clicked")


# ---------- SELECT GAME A ----------
game_a_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Game A')]"))
)

driver.execute_script("arguments[0].click();", game_a_select)

time.sleep(2)
screenshot(driver, "03_game_a_selected")


# ---------- CREATE TABLES ----------
for table_name, table_type in tables:

    print(f"Creating {table_name}")

    add_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add')]"))
    )
    driver.execute_script("arguments[0].click();", add_btn)

    time.sleep(1)
    screenshot(driver, f"{table_name}_form_open")

    # Table name
    name = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Table')]"))
    )
    name.clear()
    name.send_keys(table_name)

    # Type
    type_box = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Standard')]")
    type_box.clear()
    type_box.send_keys(table_type)

    # Prices
    p = prices[table_type]

    nums = driver.find_elements(By.XPATH, "//input[@type='number']")

    nums[0].clear()
    nums[0].send_keys(str(p[0]))

    nums[1].clear()
    nums[1].send_keys(str(p[1]))

    nums[2].clear()
    nums[2].send_keys(str(p[2]))

    nums[3].clear()
    nums[3].send_keys(str(p[3]))

    screenshot(driver, f"{table_name}_filled")

    # Create
    create = driver.find_element(By.XPATH, "//button[contains(text(),'Create')]")
    driver.execute_script("arguments[0].click();", create)

    print(f"{table_name} created")

    time.sleep(2)
    screenshot(driver, f"{table_name}_created")


print("All tables for Game A created successfully")

screenshot(driver, "04_final_result")

time.sleep(3)
driver.quit()