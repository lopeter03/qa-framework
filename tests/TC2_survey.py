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

def test_survey_form():
    driver = init_driver()
    ensure_dirs()

    steps = []
    try:
        driver.get("https://demoqa.com/automation-practice-form")

        driver.find_element(By.ID, "firstName").send_keys("David")
        steps.append(("Enter first name", "David", "Pass"))

        driver.find_element(By.ID, "lastName").send_keys("Tester")
        steps.append(("Enter last name", "Tester", "Pass"))

        driver.find_element(By.ID, "userEmail").send_keys("david@example.com")
        steps.append(("Enter email", "david@example.com", "Pass"))

        driver.find_element(By.ID, "userNumber").send_keys("1234567890")
        steps.append(("Enter mobile", "1234567890", "Pass"))

        gender_radio = driver.find_element(By.ID, "gender-radio-1")
        driver.execute_script("arguments[0].click();", gender_radio)
        steps.append(("Select gender", "Male", "Pass"))

        submit_btn = driver.find_element(By.ID, "submit")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        driver.execute_script("arguments[0].click();", submit_btn)
        steps.append(("Click submit", "Button clicked", "Pass"))

        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
        )
        assert "David Tester" in modal.text
        steps.append(("Verify modal content", "Thanks for submitting the form", "Pass"))

        driver.save_screenshot("reports/screenshots/survey_success.png")

    except Exception as e:
        steps.append(("Error", str(e), "Fail"))
        driver.save_screenshot("reports/screenshots/survey_error.png")
        raise
    finally:
        write_steps(steps)
        driver.quit()
