from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import os
import time

# abt code:
# This script automates the process of adding tables to Game C in the Snookhead web application.
# 3 tables are created with 1 standard and 2 premium, having different price values.
# its dynamic and can be easily modified to add more tables or change prices by updating the tables and prices data structures.
# It uses Selenium WebDriver to simulate user actions on the website.


# -----------------------------
# Create screenshots folder
# -----------------------------
os.makedirs("screenshots", exist_ok=True)

def take_ss(driver, name):
    driver.save_screenshot(f"screenshots/{name}.png")


# -----------------------------
# Table data for Game C
# -----------------------------
tables = [
    {"name": "Table A", "type": "Premium"},
    {"name": "Table B", "type": "Premium"},
    {"name": "Table C", "type": "Standard"}
]

prices = {
    "Standard": {"min": 18, "half": 350, "hour": 700, "frame": 60},
    "Premium": {"min": 28, "half": 480, "hour": 950, "frame": 80}
}


# -----------------------------
# Launch browser
# -----------------------------
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

#driver.get("https://snookhead-webapp.vercel.app/")
driver.get ("http://localhost:5173/")
take_ss(driver, "01_homepage")


# -----------------------------
# Login
# -----------------------------
email = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
)
password = driver.find_element(By.XPATH, "//input[@type='password']")

email.send_keys("trushajadhav25@gmail.com")
password.send_keys("a7b3SNuSUrYyDUx")

take_ss(driver, "02_login_filled")

login_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")
login_btn.click()

wait.until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]"))
)

take_ss(driver, "03_dashboard_loaded")
print("Logged in successfully")


# -----------------------------
# Hover over Game C tab and click
# -----------------------------
game_c_tab = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Game C']"))
)

actions.move_to_element(game_c_tab).perform()
time.sleep(1)
take_ss(driver, "04_hover_game_c")

driver.execute_script("arguments[0].click();", game_c_tab)
time.sleep(2)
take_ss(driver, "05_game_c_opened")

print("Game C selected")


# -----------------------------
# Click Add Tables
# -----------------------------
add_tables_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Tables')]"))
)

driver.execute_script("arguments[0].click();", add_tables_btn)
time.sleep(2)
take_ss(driver, "06_add_tables_clicked")

print("Add Tables clicked")


# -----------------------------
# If Game C selection appears again, click it
# -----------------------------
try:
    game_c_select = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Game C']"))
    )
    driver.execute_script("arguments[0].click();", game_c_select)
    time.sleep(2)
    take_ss(driver, "07_game_c_selected_again")
    print("Game C selected again from game list")
except TimeoutException:
    print("Game selection screen did not appear, continuing...")


# -----------------------------
# Create 3 tables
# -----------------------------
for i, table in enumerate(tables, start=1):
    print(f"Creating {table['name']} in Game C")

    # Click Add / Add New Table button
    add_new_table_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add')]"))
    )
    driver.execute_script("arguments[0].click();", add_new_table_btn)
    time.sleep(1)
    take_ss(driver, f"08_{i}_form_open")

    # Table Name
    table_name_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Table')]"))
    )
    table_name_input.clear()
    table_name_input.send_keys(table["name"])

    # Table Type
    table_type_input = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Standard')]")
    table_type_input.clear()
    table_type_input.send_keys(table["type"])

    # Price values based on type
    price = prices[table["type"]]

    number_inputs = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@type='number']"))
    )

    number_inputs[0].clear()
    number_inputs[0].send_keys(str(price["min"]))

    number_inputs[1].clear()
    number_inputs[1].send_keys(str(price["half"]))

    number_inputs[2].clear()
    number_inputs[2].send_keys(str(price["hour"]))

    number_inputs[3].clear()
    number_inputs[3].send_keys(str(price["frame"]))

    take_ss(driver, f"09_{table['name']}_filled")

    # Click Create
    create_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create')]"))
    )
    driver.execute_script("arguments[0].click();", create_btn)

    time.sleep(2)
    take_ss(driver, f"10_{table['name']}_created")

    print(f"{table['name']} created successfully")


take_ss(driver, "11_final_game_c_tables")
print("All 3 tables created for Game C")

time.sleep(5)
driver.quit()