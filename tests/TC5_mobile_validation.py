import pytest, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.driver_setup import init_driver

def ensure_dirs():
    os.makedirs("reports/screenshots", exist_ok=True)

def test_mobile_validation():
    driver = init_driver()
    ensure_dirs()
    screenshot_path = "reports/screenshots/mobile_invalid.png"
    try:
        # Navigate to a sample form page (replace with your actual form URL)
        driver.get("https://the-internet.herokuapp.com/login")

        # Enter invalid mobile number into username field (simulating phone input)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys("123abc")  # invalid mobile format

        # Enter dummy password
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys("dummy123")

        # Click login (acting as form submit)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))
        ).click()

        # Verify error message (adjust text to match your form’s validation)
        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "Your username is invalid!" in message.text

        # Save screendump
        driver.save_screenshot(screenshot_path)
        print(f"Screendump saved: {screenshot_path}")

    except Exception as e:
        driver.save_screenshot("reports/screenshots/mobile_invalid_error.png")
        print("Error occurred, screenshot saved as mobile_invalid_error.png")
        raise
    finally:
        driver.quit()
