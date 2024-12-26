# qa_selenium_test.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Configuration for running tests
BROWSER = "chrome"  # Change to "firefox" for Firefox

@pytest.fixture(scope="module")
def driver():
    """Fixture to initialize and quit the Selenium WebDriver."""
    if BROWSER.lower() == "chrome":
        options = ChromeOptions()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif BROWSER.lower() == "firefox":
        options = FirefoxOptions()
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {BROWSER}")

    driver.maximize_window()
    yield driver
    driver.quit()

def test_search_functionality(driver):
    """Test to validate search functionality on the Selenium Playground Table Search Demo."""
    # Navigate to the Selenium Playground Table Search Demo
    url = "https://www.seleniumeasy.com/test/table-search-filter-demo.html"
    driver.get(url)

    # Locate the search box and search for "New York"
    search_box = driver.find_element(By.ID, "task-table-filter")
    search_box.send_keys("New York")

    # Validate the search results
    rows = driver.find_elements(By.XPATH, "//table[@id='task-table']/tbody/tr")
    visible_rows = [row for row in rows if row.is_displayed()]

    assert len(visible_rows) == 5, f"Expected 5 entries, but found {len(visible_rows)}"

    # Verify total entries (static check for 24 total entries)
    assert len(rows) == 24, f"Expected 24 total entries in the table, but found {len(rows)}"

if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", "qa_selenium_test.py"])
