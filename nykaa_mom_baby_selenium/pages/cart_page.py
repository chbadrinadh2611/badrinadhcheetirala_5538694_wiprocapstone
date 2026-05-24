from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class CartPage(BasePage):
    """Page object for Nykaa Shopping Bag (Cart) Page."""

    # Locators
    BAG_ICON = (By.XPATH,
        "//span[contains(text(),'Bag')] | "
        "//a[contains(@href,'bag')] | "
        "//div[contains(@class,'bag')] | "
        "//span[contains(@class,'bag')]"
    )
    CART_ITEMS = (By.XPATH,
        "//div[contains(@class,'cart-item')] | "
        "//div[contains(@class,'bag-item')] | "
        "//div[contains(@class,'CartItem')]"
    )
    CART_PRODUCT_NAME = (By.XPATH,
        "//div[contains(@class,'cart-item')]//span[contains(@class,'name')] | "
        "//div[contains(@class,'bag')]//p[contains(@class,'name')]"
    )
    EMPTY_CART_MSG = (By.XPATH,
        "//div[contains(text(),'Your bag is empty')] | "
        "//p[contains(text(),'empty')] | "
        "//span[contains(text(),'empty')]"
    )
    PROCEED_TO_BUY = (By.XPATH,
        "//button[contains(text(),'PROCEED TO BUY')] | "
        "//button[contains(text(),'Proceed to Buy')] | "
        "//a[contains(text(),'Proceed')]"
    )
    REMOVE_ITEM_BTN = (By.XPATH,
        "(//button[contains(text(),'Remove')] | "
        "//span[contains(text(),'REMOVE')])[1]"
    )
    CART_TOTAL = (By.XPATH,
        "//span[contains(@class,'total')] | "
        "//div[contains(text(),'Total')]//following-sibling::*"
    )
    QUANTITY_INPUT = (By.XPATH, "//input[@type='number'] | //select[contains(@class,'qty')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open_cart(self):
        """Click on the Bag icon to open cart."""
        bag = self.wait.until(EC.element_to_be_clickable(self.BAG_ICON))
        bag.click()
        time.sleep(3)

    def navigate_to_cart(self):
        """Directly navigate to cart URL."""
        self.driver.get("https://www.nykaa.com/bag")
        time.sleep(3)

    def is_cart_page(self):
        """Verify we are on the cart/bag page."""
        return "bag" in self.driver.current_url.lower()

    def get_cart_item_count(self):
        """Return number of items in cart."""
        try:
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(items)
        except Exception:
            return 0

    def is_cart_empty(self):
        """Check if cart is empty."""
        return self.is_element_present(*self.EMPTY_CART_MSG, timeout=5)

    def is_product_in_cart(self, product_name_keyword):
        """Check if specific product appears in cart."""
        try:
            cart_text = self.driver.find_element(By.XPATH, "//body").text
            return product_name_keyword.lower() in cart_text.lower()
        except Exception:
            return False

    def get_cart_total(self):
        """Return cart total amount text."""
        try:
            return self.get_text(*self.CART_TOTAL)
        except Exception:
            return "Total not found"

    def click_proceed_to_buy(self):
        """Click Proceed to Buy button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.PROCEED_TO_BUY))
        btn.click()
        time.sleep(3)
