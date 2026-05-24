from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for Nykaa Home Page."""

    # Locators
    LOGIN_ICON = (By.XPATH, "//a[contains(@href,'login')] | //span[contains(text(),'Sign In')] | //div[contains(@class,'user-section')]//a")
    MOM_BABY_NAV = (By.XPATH, "//a[contains(text(),'Mom') and contains(text(),'Baby')] | //span[contains(text(),'Mom & Baby')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self, url):
        """Open Nykaa homepage."""
        self.driver.get(url)
        self.driver.maximize_window()

    def navigate_to_mom_baby(self, mom_baby_url):
        """Directly navigate to Mom & Baby category URL."""
        self.driver.get(mom_baby_url)

    def verify_homepage(self):
        """Verify we are on Nykaa homepage."""
        return "Nykaa" in self.driver.title
