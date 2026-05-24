import pytest, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.driver_setup import init_driver

def ensure_dirs():
    os.makedirs("reports/screenshots", exist_ok=True)

def test_boundary_validation():
    driver = init_driver()
    ensure_dirs()
    screenshot_path = "reports/screenshots/boundary_validation.png"
    try:
        # Navigate to login page
        driver.get("https://the-internet.herokuapp.com/login")

        # Enter overly long username (boundary test)
        long_username = "A" * 256  # 256 characters
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(long_username)

        # Enter overly long password
        long_password = "B" * 256
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys(long_password)

        # Submit form
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))
        ).click()

        # Verify error message appears
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "Your username is invalid!" in error_message.text or "Your password is invalid!" in error_message.text

        # Save screendump
        driver.save_screenshot(screenshot_path)
        print(f"Screendump saved: {screenshot_path}")

    except Exception as e:
        driver.save_screenshot("reports/screenshots/boundary_validation_error.png")
        print("Error occurred, screenshot saved as boundary_validation_error.png")
        raise
    finally:
        driver.quit()
