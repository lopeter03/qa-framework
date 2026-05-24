import pytest, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.driver_setup import init_driver

def ensure_dirs():
    os.makedirs("reports/screenshots", exist_ok=True)

def test_xss_prevention():
    driver = init_driver()
    ensure_dirs()
    screenshot_path = "reports/screenshots/xss_prevention.png"
    try:
        # Navigate to login page
        driver.get("https://the-internet.herokuapp.com/login")

        # Enter XSS payload as username
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys("<script>alert('XSS')</script>")

        # Enter dummy password
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys("anything")

        # Submit form
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))
        ).click()

        # Verify error message appears (no script execution)
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "Your username is invalid!" in error_message.text

        # Save screendump
        driver.save_screenshot(screenshot_path)
        print(f"Screendump saved: {screenshot_path}")

    except Exception as e:
        driver.save_screenshot("reports/screenshots/xss_prevention_error.png")
        print("Error occurred, screenshot saved as xss_prevention_error.png")
        raise
    finally:
        driver.quit()
