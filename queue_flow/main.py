from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

# Summary:
# This script automates the queue flow in the Snookhead web application.
# It logs in, books multiple tables using existing members, adds a member to the queue,
# waits for Table A to finish its session, clicks Seat Next from the popup,
# waits for the new session to start, and then returns to the queue page.
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


def click_ok_popup(driver, wait):
    try:
        ok_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[normalize-space()='OK' or normalize-space()='Ok']"
            ))
        )
        click_js(driver, ok_btn)
        print("OK popup handled")
        time.sleep(2)
        return True
    except:
        print("No OK popup found")
        return False


def wait_for_session_end_popup(driver, wait, max_wait=180):
    try:
        print("Waiting for session-end popup...")

        ok_btn = WebDriverWait(driver, max_wait).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[normalize-space()='OK' or normalize-space()='Ok']"
            ))
        )

        click_js(driver, ok_btn)
        print("Session-end popup handled")
        ss(driver, "session_end_popup_handled")
        time.sleep(2)
        return True

    except TimeoutException:
        print("Session-end popup did not appear in time")
        return False


# ---------- CORE FUNCTIONS ----------
def login(driver, wait):
    driver.get("http://localhost:5173/")

    email = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
    )
    password = driver.find_element(By.XPATH, "//input[@type='password']")

    email.send_keys("trushajadhav25@gmail.com")
    password.send_keys("trusha25")

    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dashboard')]"))
    )

    print("Login done")
    ss(driver, "01_dashboard")


# ---------- OPTIONAL: MEMBER CREATION ----------
# Keep these commented if members are already created in the app

# def open_new_member_popup(driver, wait):
#     new_member_btn = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'New Member')]"))
#     )
#     click_js(driver, new_member_btn)
#     print("New Member popup opened")
#     time.sleep(2)
#     ss(driver, "02_new_member_popup")


# def create_member(driver, wait, name, phone, address):
#     open_new_member_popup(driver, wait)

#     name_input = wait.until(
#         EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter name']"))
#     )
#     name_input.clear()
#     name_input.send_keys(name)

#     phone_input = wait.until(
#         EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter phone']"))
#     )
#     phone_input.clear()
#     phone_input.send_keys(phone)

#     address_input = wait.until(
#         EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter address']"))
#     )
#     address_input.clear()
#     address_input.send_keys(address)

#     ss(driver, f"member_{name}_filled")

#     add_member_btn = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Member')]"))
#     )
#     click_js(driver, add_member_btn)

#     print(f"Member created: {name}")
#     time.sleep(2)
#     click_ok_popup(driver, wait)
#     ss(driver, f"member_{name}_created")


def select_table(driver, wait, table_name):
    table_card = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//div[contains(@class,'table-card') and .//*[contains(text(),'{table_name}')]]"
        ))
    )
    click_js(driver, table_card)
    time.sleep(2)
    print(f"{table_name} selected")
    ss(driver, f"{table_name}_selected")


def book_table(driver, wait, table_name, member_name="battata_wada", time_value="2"):
    select_table(driver, wait, table_name)

    customer = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//label[text()='Customer Name']/following::input[1]"
        ))
    )
    customer.clear()
    customer.send_keys(member_name[:2].lower())
    time.sleep(2)

    member = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//li[contains(@class,'autocomplete-item') and contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{member_name.lower()}')]"
        ))
    )
    click_js(driver, member)

    time_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
    )
    time_input.clear()
    time_input.send_keys(time_value)

    ss(driver, f"{table_name}_booking_filled")

    confirm_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class,'book-btn-unified') or contains(text(),'Confirm Booking')]"
        ))
    )
    click_js(driver, confirm_btn)

    print(f"{table_name} booked")
    time.sleep(2)
    click_ok_popup(driver, wait)
    ss(driver, f"{table_name}_booked")

    go_to_dashboard(driver, wait)


def go_to_dashboard(driver, wait):
    dashboard = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Dashboard')]"))
    )
    click_js(driver, dashboard)
    time.sleep(2)
    ss(driver, "dashboard_return")


def open_queue_page(driver, wait):
    queue_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Queue']"))
    )
    click_js(driver, queue_btn)
    time.sleep(2)
    print("Queue page opened")
    ss(driver, "queue_page")


def open_game_b_in_queue(driver, wait):
    game_b = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Game B')]"))
    )
    click_js(driver, game_b)
    time.sleep(2)
    print("Game B opened in Queue")
    ss(driver, "queue_game_b")


def add_to_queue(driver, wait, member_name="battata_wada", phone="8446718788", time_value="2"):
    add_to_q_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add to Q')]"))
    )
    click_js(driver, add_to_q_btn)
    time.sleep(2)
    ss(driver, "add_to_q_popup")

    customer_input = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[contains(@class,'queue-modal')]//input[contains(@class,'autocomplete-input')]"
        ))
    )
    customer_input.clear()
    customer_input.send_keys(member_name[:2].lower())
    time.sleep(2)
    ss(driver, "queue_name_typed")

    member = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "(//li[contains(@class,'autocomplete-item') and not(contains(@class,'add-new-member'))])[1]"
        ))
    )
    click_js(driver, member)
    time.sleep(1)
    ss(driver, "queue_member_selected")

    phone_input = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[contains(@class,'queue-modal')]//input[@placeholder='Enter phone number' or contains(@placeholder,'phone')]"
        ))
    )
    phone_input.clear()
    phone_input.send_keys(phone)

    time_input = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[contains(@class,'queue-modal')]//input[@type='number']"
        ))
    )
    time_input.clear()
    time_input.send_keys(time_value)

    ss(driver, "queue_details_filled")

    confirm_q_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'queue-modal')]//button[contains(text(),'Add to Q')]"
        ))
    )
    click_js(driver, confirm_q_btn)

    print("Added to queue")
    time.sleep(2)
    click_ok_popup(driver, wait)
    ss(driver, "queue_added")


def wait_for_table_release_and_seat_next(driver, wait, popup_wait=180):
    go_to_dashboard(driver, wait)

    print("Waiting for Seat Next popup after Table A session ends...")

    seat_next_popup_btn = WebDriverWait(driver, popup_wait).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(text(),'Seat Now')]"
        ))
    )

    click_js(driver, seat_next_popup_btn)
    print("Seat Next clicked from popup")
    time.sleep(2)
    ss(driver, "seat_next_popup_clicked")

    # wait a little so Table A becomes occupied again
    print("Waiting for Table A to become occupied again...")
    time.sleep(10)
    ss(driver, "table_a_reoccupied")

    # now wait only 60 sec more, no need to wait for other tables
    print("Waiting 60 seconds...")
    time.sleep(60)
    ss(driver, "after_60_sec")

    # go back to queue
    queue_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Queue')]"))
    )
    click_js(driver, queue_btn)
    time.sleep(2)
    ss(driver, "back_to_queue")

    print("Returned to Queue page")

# ---------- RUN ----------
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    login(driver, wait)

    # ---------- OPTIONAL MEMBER CREATION ----------
    # Uncomment only if members are NOT already added in the app
    # create_member(driver, wait, "gulabjamun1", "9960570621", "Mumbai")
    # create_member(driver, wait, "Jelebi", "9921500400", "kerala")

    # ---------- BOOK TABLES USING EXISTING MEMBERS ----------
    book_table(driver, wait, "Table A", member_name="gulabjamun1", time_value="1")
    book_table(driver, wait, "Table B", member_name="Jelebi", time_value="7")
    book_table(driver, wait, "Table C", member_name="battata_wada", time_value="7")

    # ---------- ADD TO QUEUE ----------
    open_queue_page(driver, wait)
    open_game_b_in_queue(driver, wait)
    add_to_queue(driver, wait, member_name="battata_wada", phone="8446718788", time_value="1")

    # ---------- WAIT FOR TABLE RELEASE ----------
    wait_for_table_release_and_seat_next(driver, wait, popup_wait=180)

    print("Queue flow test completed successfully")

finally:
    time.sleep(3)
    driver.quit()