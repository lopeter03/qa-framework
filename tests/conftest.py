import sys
import os
import pytest

# Always add the project root (qa-framework) to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Shared driver fixture for all test cases (TC1–TC10)
@pytest.fixture(scope="function")
def driver():
    from src.driver_setup import init_driver
    driver = init_driver()
    yield driver
    driver.quit()

# Utility fixture to ensure screenshot folder exists
@pytest.fixture(scope="session", autouse=True)
def ensure_dirs():
    os.makedirs("reports/screenshots", exist_ok=True)
