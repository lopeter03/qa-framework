import pytest, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.driver_setup import init_driver

def ensure_dirs():
    os.makedirs("reports/screenshots", exist_ok=True)

def test_login_invalid():
    driver = init_driver()
    ensure_dirs()
    screenshot_path = "reports/screenshots/login_invalid.png"
    try:
        driver.get("https://the-internet.herokuapp.com/login")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys("wronguser")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys("wrongpassword")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))
        ).click()

        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "Your username is invalid!" in message.text

        # Always save screenshot if we reach here
        driver.save_screenshot(screenshot_path)
        print(f"Screendump saved: {screenshot_path}")

    except Exception as e:
        # Save screenshot even on failure
        driver.save_screenshot("reports/screenshots/login_invalid_error.png")
        print("Error occurred, screenshot saved as login_invalid_error.png")
        raise
    finally:
        driver.quit()
