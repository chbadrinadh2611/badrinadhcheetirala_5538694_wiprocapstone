import allure
from pages.locators import (
    ADD_TO_BAG_BTN, CART_BTN, PROCEED_BTN,
    GUEST_CHECKOUT, NAME_FIELD, MOBILE_FIELD,
    PINCODE_FIELD, ADDRESS_FIELD, SAVE_ADDRESS_BTN
)
from utils.waits import (
    wait_for_clickable, wait_for_element,
    retry_click, scroll_into_view, js_click, short_sleep
)
from utils.screenshot_utils import (
    screenshot_before_click, screenshot_after_click,
    screenshot_on_failure, screenshot_on_success
)
from utils.logger import get_logger

logger = get_logger("CheckoutPage")


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Add product to bag")
    def add_to_bag(self):
        logger.info("Adding product to bag")
        try:
            element = retry_click(self.driver, ADD_TO_BAG_BTN)
            screenshot_on_success(self.driver, "added_to_bag")
            short_sleep(2)
            logger.info("Product added to bag")
            return element
        except Exception as e:
            screenshot_on_failure(self.driver, "add_to_bag_fail")
            logger.error(f"Failed to add to bag: {e}")
            raise

    @allure.step("Open cart")
    def open_cart(self):
        logger.info("Opening cart")
        try:
            element = wait_for_clickable(self.driver, CART_BTN)
            scroll_into_view(self.driver, element)
            screenshot_before_click(self.driver, "open_cart")
            js_click(self.driver, element)
            screenshot_after_click(self.driver, "open_cart")
            short_sleep(2)
            logger.info("Cart opened")
        except Exception as e:
            screenshot_on_failure(self.driver, "open_cart_fail")
            logger.error(f"Failed to open cart: {e}")
            raise

    @allure.step("Click Proceed")
    def click_proceed(self):
        logger.info("Clicking Proceed button")
        try:
            retry_click(self.driver, PROCEED_BTN)
            screenshot_on_success(self.driver, "proceed_clicked")
            short_sleep(2)
            logger.info("Proceed clicked")
        except Exception as e:
            screenshot_on_failure(self.driver, "proceed_fail")
            logger.error(f"Failed to click Proceed: {e}")
            raise

    @allure.step("Continue as Guest")
    def continue_as_guest(self):
        logger.info("Clicking Continue as Guest")
        try:
            retry_click(self.driver, GUEST_CHECKOUT)
            screenshot_on_success(self.driver, "guest_checkout")
            short_sleep(2)
            logger.info("Continued as guest")
        except Exception as e:
            screenshot_on_failure(self.driver, "guest_checkout_fail")
            logger.error(f"Failed to continue as guest: {e}")
            raise

    @allure.step("Fill address form")
    def fill_address(self, name, mobile, pincode, address):
        logger.info("Filling address form")
        try:
            wait_for_element(self.driver, NAME_FIELD).send_keys(name)
            wait_for_element(self.driver, MOBILE_FIELD).send_keys(mobile)
            wait_for_element(self.driver, PINCODE_FIELD).send_keys(pincode)
            wait_for_element(self.driver, ADDRESS_FIELD).send_keys(address)
            screenshot_on_success(self.driver, "address_filled")
            logger.info("Address form filled")
        except Exception as e:
            screenshot_on_failure(self.driver, "fill_address_fail")
            logger.error(f"Failed to fill address: {e}")
            raise

    @allure.step("Save address")
    def save_address(self):
        logger.info("Saving address")
        try:
            element = wait_for_clickable(self.driver, SAVE_ADDRESS_BTN)
            scroll_into_view(self.driver, element)
            screenshot_before_click(self.driver, "save_address")
            js_click(self.driver, element)
            screenshot_after_click(self.driver, "save_address")
            short_sleep(2)
            logger.info("Address saved")
        except Exception as e:
            screenshot_on_failure(self.driver, "save_address_fail")
            logger.error(f"Failed to save address: {e}")
            raise

    def get_page_text(self):
        body = self.driver.find_element("tag name", "body").text.lower()
        logger.info("Page body text retrieved")
        return body