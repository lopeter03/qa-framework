import pytest, time, os, csv
from src.driver_setup import init_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOG_FILE = "reports/test_log.csv"

def ensure_dirs():
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    # Add header if file doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Item", "Value", "Status", "Date Timestamp"])

def write_steps(steps):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for step in steps:
            writer.writerow([step[0], step[1], step[2], time.strftime("%Y/%m/%d %H:%M")])

def test_login():
    driver = init_driver()
    ensure_dirs()

    steps = []
    try:
        driver.get("https://the-internet.herokuapp.com/login")

        driver.find_element(By.ID, "username").send_keys("tomsmith")
        steps.append(("Enter username", "tomsmith", "Pass"))

        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        steps.append(("Enter password", "********", "Pass"))

        driver.find_element(By.CSS_SELECTOR, "button.radius").click()
        steps.append(("Click login", "Button clicked", "Pass"))

        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "You logged into a secure area!" in message.text
        steps.append(("Verify login success", "You logged into a secure area!", "Pass"))

        driver.save_screenshot("reports/screenshots/login_success.png")

    except Exception as e:
        steps.append(("Error", str(e), "Fail"))
        driver.save_screenshot("reports/screenshots/login_error.png")
        raise
    finally:
        write_steps(steps)
        driver.quit()
