from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# create screenshot folder
os.makedirs("screenshots", exist_ok=True)

def take_ss(driver, name):
    driver.save_screenshot(f"screenshots/{name}.png")


driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

driver.get("https://snookhead-webapp.vercel.app/")

take_ss(driver,"01_homepage")

# Login
email = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@type='email']")))
password = driver.find_element(By.XPATH,"//input[@type='password']")

email.send_keys("trushajadhav25@gmail.com")
password.send_keys("a7b3SNuSUrYyDUx")

take_ss(driver,"02_login_filled")

driver.find_element(By.XPATH,"//button[contains(text(),'Login')]").click()

# Go to Setup
wait.until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Setup')]"))).click()

take_ss(driver,"03_setup_page")

games = ["Game A","Game B","Game C"]

file = open("games.txt","w")

for game in games:

    wait.until(
        EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Add New Game')]"))
    ).click()

    take_ss(driver,f"{game}_form_open")

    game_input = wait.until(
        EC.element_to_be_clickable((By.XPATH,"//input[@placeholder='e.g., Snooker, Pool, 8-Ball']"))
    )

    game_input.clear()
    game_input.send_keys(game)

    take_ss(driver,f"{game}_name_entered")

    driver.find_element(By.XPATH,"//button[contains(text(),'Create Game')]").click()

    print("Created:",game)

    file.write(game+"\n")

    take_ss(driver,f"{game}_created")

    time.sleep(2)

file.close()

take_ss(driver,"04_all_games_created")

driver.quit()