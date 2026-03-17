from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# This script automates game deletion in the Snookhead web app.
# It logs in, navigates to the Set up menu, enters edit mode,
# deletes the selected game (Game A), and confirms the deletion.
# Screenshots are captured during the process.


os.makedirs("screenshots", exist_ok=True)

def take_ss(driver, name):
    driver.save_screenshot(f"screenshots/{name}.png")

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

driver.get("http://localhost:5173/")
# driver.get("https://snookhead-webapp.vercel.app/")

# Login
email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
password = driver.find_element(By.XPATH, "//input[@type='password']")

email.send_keys("trushajadhav25@gmail.com")
password.send_keys("trusha25")

driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

# Click Set up menu
setup_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Set up menu')]"))
)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", setup_menu)
time.sleep(1)
driver.execute_script("arguments[0].click();", setup_menu)

print("Clicked Set up menu")
time.sleep(2)
take_ss(driver, "setup_menu_opened")

# Click Edit button
edit_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Edit')]"))
)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_btn)
time.sleep(1)
driver.execute_script("arguments[0].click();", edit_btn)

print("Clicked Edit")
time.sleep(2)
take_ss(driver, "edit_clicked")

# ---------- CLICK DELETE BUTTON FOR GAME A ----------

delete_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'setup-card-item') and .//*[contains(text(),'Game A')]]//button[contains(@class,'delete')]"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", delete_btn)
time.sleep(1)
driver.execute_script("arguments[0].click();", delete_btn)

print("Delete icon clicked for Game A")
take_ss(driver, "delete_icon_clicked")
time.sleep(2)

# Confirm delete in popup
confirm_delete = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Delete')]"))
)
driver.execute_script("arguments[0].click();", confirm_delete)

print("Confirmed delete")
take_ss(driver, "delete_confirmed")
time.sleep(2)

# Exit
driver.quit()
print("Browser closed")