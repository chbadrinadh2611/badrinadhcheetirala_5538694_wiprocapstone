from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class BasePage:
    """Base page class with common utility methods for all page objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find(self, by, value):
        """Wait until element is visible and return it."""
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click(self, by, value):
        """Wait until element is clickable and click it."""
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def get_text(self, by, value):
        """Return text content of the element."""
        return self.find(by, value).text

    def send_keys(self, by, value, text):
        """Clear field and type text."""
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)

    def is_element_present(self, by, value, timeout=10):
        """Check if element is present within given timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    def take_screenshot(self, name):
        """Save a screenshot to screenshots folder."""
        path = f"screenshots/{name}.png"
        self.driver.save_screenshot(path)
        return path

    def scroll_into_view(self, element):
        """Scroll element into view using JS."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
