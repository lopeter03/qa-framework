import pytest, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.driver_setup import init_driver

def ensure_dirs():
    os.makedirs("reports/screenshots", exist_ok=True)

def test_password_validation():
    driver = init_driver()
    ensure_dirs()
    screenshot_path = "reports/screenshots/password_invalid.png"
    try:
        # Navigate to demo login page
        driver.get("https://the-internet.herokuapp.com/login")

        # Enter valid username
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys("tomsmith")

        # Enter invalid password (too short, e.g. '123')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys("123")

        # Submit form
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))
        ).click()

        # Verify error message
        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "Your password is invalid!" in message.text

        # Save screendump
        driver.save_screenshot(screenshot_path)
        print(f"Screendump saved: {screenshot_path}")

    except Exception as e:
        driver.save_screenshot("reports/screenshots/password_invalid_error.png")
        print("Error occurred, screenshot saved as password_invalid_error.png")
        raise
    finally:
        driver.quit()
