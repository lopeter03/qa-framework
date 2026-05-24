import pytest, os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.driver_setup import init_driver

def ensure_dirs():
    os.makedirs("reports/screenshots", exist_ok=True)

def test_session_timeout():
    driver = init_driver()
    ensure_dirs()
    screenshot_path = "reports/screenshots/session_timeout.png"
    try:
        # Navigate to login page
        driver.get("https://the-internet.herokuapp.com/login")

        # Enter valid credentials
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys("tomsmith")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys("SuperSecretPassword!")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))
        ).click()

        # Verify login success by waiting for flash message
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "You logged into a secure area!" in success_message.text

        # Simulate idle timeout (shortened for demo, e.g. 10s instead of 65s)
        time.sleep(10)

        # Manually log out to simulate timeout
        driver.get("https://the-internet.herokuapp.com/logout")

        # Verify forced logout message
        logout_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "You logged out of the secure area!" in logout_message.text

        # Save screendump
        driver.save_screenshot(screenshot_path)
        print(f"Screendump saved: {screenshot_path}")

    except Exception as e:
        driver.save_screenshot("reports/screenshots/session_timeout_error.png")
        print("Error occurred, screenshot saved as session_timeout_error.png")
        raise
    finally:
        driver.quit()
