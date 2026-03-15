from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# abt code:
# This script automates the process of adding tables to Game C in the Snookhead web application.
# 3 tables are created with 2 standard and 1 premium, having different price values.
# its dynamic and can be easily modified to add more tables or change prices by updating the tables and prices data structures.
# It uses Selenium WebDriver to simulate user actions on the website.

# ---------- Screenshot Folder ----------
os.makedirs("screenshots", exist_ok=True)

def screenshot(driver,name):
    driver.save_screenshot(f"screenshots/{name}.png")


# ---------- TABLE DATA ----------

tables = [
    ("Table A","Standard"),
    ("Table B","Standard"),
    ("Table C","Premium")
]

prices = {
    "Standard":(10,300,600,50),
    "Premium":(20,400,800,70)
}


# ---------- BROWSER ----------

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver,20)


#driver.get("https://snookhead-webapp.vercel.app/")
driver.get ("http://localhost:5173/")


# ---------- LOGIN ----------

email = wait.until(
    EC.presence_of_element_located((By.XPATH,"//input[@type='email']"))
)

password = driver.find_element(By.XPATH,"//input[@type='password']")

email.send_keys("trushajadhav25@gmail.com")
password.send_keys("a7b3SNuSUrYyDUx")

driver.find_element(By.XPATH,"//button[contains(text(),'Login')]").click()

wait.until(
    EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Dashboard')]"))
)

screenshot(driver,"dashboard")


# ---------- ADD TABLES ----------

add_tables = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Add Tables')]"))
)

add_tables.click()


# ---------- SELECT GAME ----------

game = wait.until(
    EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Game A')]"))
)

game.click()


# ---------- CREATE TABLES ----------

for table_name,table_type in tables:

    add = wait.until(
        EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Add')]"))
    )

    add.click()

    name = wait.until(
        EC.presence_of_element_located((By.XPATH,"//input[contains(@placeholder,'Table')]"))
    )

    name.send_keys(table_name)


    type_box = driver.find_element(
        By.XPATH,"//input[contains(@placeholder,'Standard')]"
    )

    type_box.clear()
    type_box.send_keys(table_type)


    p = prices[table_type]

    nums = driver.find_elements(By.XPATH,"//input[@type='number']")

    nums[0].send_keys(p[0])
    nums[1].send_keys(p[1])
    nums[2].send_keys(p[2])
    nums[3].send_keys(p[3])

    screenshot(driver,table_name)

    create = driver.find_element(
        By.XPATH,"//button[contains(text(),'Create')]"
    )

    create.click()

    time.sleep(2)


print("Tables created successfully")

time.sleep(3)

driver.quit()