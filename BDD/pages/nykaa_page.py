import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pages.locators import (
    URL, PRODUCTS, ADD_TO_BAG_XPATHS, BAG_ICON_XPATHS,
    PROCEED_XPATHS, GUEST_CHECKOUT, SHIP_ADDRESS_XPATHS,
    PINCODE_FIELD, HOUSE_FIELD, ROAD_FIELD,
    NAME_FIELD, PHONE_FIELD, EMAIL_FIELD
)
from utils.logger import get_logger
from utils.screenshot_utils import screenshot_on_success, screenshot_on_failure

logger = get_logger("NykaaPage")


class NykaaPage:
    def __init__(self, driver):
        self.driver = driver

    # ── Open Page ──────────────────────────────────────────────────
    @allure.step("Open Nykaa Baby Care page")
    def open_page(self):
        logger.info(f"Opening page: {URL}")
        self.driver.get(URL)
        time.sleep(5)
        logger.info(f"Current URL: {self.driver.current_url}")
        logger.info(f"Page title: {self.driver.title}")
        screenshot_on_success(self.driver, "page_opened")

    # ── Get Products ───────────────────────────────────────────────
    @allure.step("Get products from page")
    def get_products(self):
        time.sleep(2)
        items = self.driver.find_elements(By.XPATH, "//a[contains(@href,'/p/')]")
        logger.info(f"Product count: {len(items)}")
        return items

    # ── Expand Filter ──────────────────────────────────────────────
    @allure.step("Expand filter: {filter_name}")
    def expand_filter(self, filter_name):
        logger.info(f"Expanding filter: {filter_name}")
        try:
            elements = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH,
                    f"//div[normalize-space(text())='{filter_name}'] | "
                    f"//p[normalize-space(text())='{filter_name}'] | "
                    f"//span[normalize-space(text())='{filter_name}']"
                ))
            )
            for index, el in enumerate(elements):
                try:
                    if el.is_displayed():
                        logger.info(f"{filter_name} visible at index {index}")
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});", el)
                        time.sleep(2)
                        self.driver.execute_script("arguments[0].click();", el)
                        time.sleep(3)
                        logger.info(f"{filter_name} expanded")
                        screenshot_on_success(self.driver, f"filter_{filter_name}_expanded")
                        return True
                except Exception as e:
                    logger.warning(f"Retry at index {index}: {e}")
            return False
        except Exception as e:
            logger.error(f"Expand filter failed: {e}")
            screenshot_on_failure(self.driver, f"filter_{filter_name}_fail")
            return False

    # ── Click Filter Option ────────────────────────────────────────
    @allure.step("Click filter option: {option}")
    def click_filter_option(self, option):
        logger.info(f"Selecting option: {option}")
        try:
            # Convert to lowercase for case-insensitive matching
            # Nykaa shows "4 stars & above" in lowercase on the page
            option_lower = option.lower()

            xpath = (
                f"//label[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{option_lower}')] | "
                f"//span[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{option_lower}')] | "
                f"//div[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{option_lower}')]"
            )

            elements = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            logger.info(f"Found {len(elements)} elements for option: {option}")

            for index, el in enumerate(elements):
                try:
                    if el.is_displayed():
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});", el)
                        time.sleep(2)
                        WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(el))
                        self.driver.execute_script("arguments[0].click();", el)
                        logger.info(f"Clicked option: {option} at index {index}")
                        time.sleep(5)
                        screenshot_on_success(self.driver, f"option_{option_lower}_selected")
                        return True
                except Exception as e:
                    logger.warning(f"Retry index {index}: {e}")

            logger.error(f"Option not clickable: {option}")
            return False

        except Exception as e:
            logger.error(f"Click filter option failed '{option}': {e}")
            screenshot_on_failure(self.driver, f"option_{option}_fail")
            return False

    # ── Click First Product ────────────────────────────────────────
    @allure.step("Click first product")
    def click_first_product(self):
        logger.info("Clicking first product")
        products = self.get_products()
        assert len(products) > 0, "No products found"
        first_url = products[0].get_attribute("href")
        logger.info(f"Opening product: {first_url}")
        self.driver.get(first_url)
        time.sleep(5)
        screenshot_on_success(self.driver, "product_page_opened")

    # ── Add To Bag ─────────────────────────────────────────────────
    @allure.step("Add product to bag")
    def add_to_bag(self):
        logger.info("Adding product to bag")
        for xpath in ADD_TO_BAG_XPATHS:
            try:
                btn = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                if btn.is_displayed():
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", btn)
                    logger.info(f"Add to Bag clicked via: {xpath}")
                    time.sleep(5)
                    screenshot_on_success(self.driver, "added_to_bag")
                    return True
            except Exception:
                continue
        logger.error("Add to Bag button not found")
        screenshot_on_failure(self.driver, "add_to_bag_fail")
        return False

    # ── Open Bag ───────────────────────────────────────────────────
    @allure.step("Open bag sidebar")
    def open_bag(self):
        logger.info("Opening bag")
        if self._is_bag_open():
            logger.info("Bag already open")
            return True
        for xpath in BAG_ICON_XPATHS:
            try:
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                if el.is_displayed():
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(3)
                    logger.info(f"Bag icon clicked via: {xpath}")
                    screenshot_on_success(self.driver, "bag_opened")
                    return True
            except Exception:
                continue
        logger.error("Bag icon not found")
        screenshot_on_failure(self.driver, "bag_open_fail")
        return False

    def _is_bag_open(self):
        try:
            body = self.driver.find_element(By.XPATH, "//body").text.lower()
            return any(k in body for k in ["you pay", "grand total", "proceed", "bag mrp"])
        except Exception:
            return False

    # ── Proceed ────────────────────────────────────────────────────
    @allure.step("Click Proceed button")
    def click_proceed(self):
        logger.info("Clicking Proceed")
        iframe_switched = False
        try:
            iframes = self.driver.find_elements(
                By.XPATH, "//iframe[contains(@src,'cart') or contains(@class,'cart')]")
            if iframes:
                self.driver.switch_to.frame(iframes[0])
                iframe_switched = True
        except Exception:
            pass

        for xpath in PROCEED_XPATHS:
            try:
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                if el.is_displayed():
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", el)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(4)
                    logger.info(f"Proceed clicked: {xpath}")
                    screenshot_on_success(self.driver, "proceed_clicked")
                    if iframe_switched:
                        self.driver.switch_to.default_content()
                    return True
            except Exception:
                continue

        if iframe_switched:
            self.driver.switch_to.default_content()
        logger.error("Proceed button not found")
        screenshot_on_failure(self.driver, "proceed_fail")
        return False

    # ── Continue As Guest ──────────────────────────────────────────
    @allure.step("Continue as Guest")
    def continue_as_guest(self):
        logger.info("Clicking Continue as Guest")
        try:
            time.sleep(3)
            guest_btn = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(GUEST_CHECKOUT))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", guest_btn)
            time.sleep(1.5)
            try:
                ActionChains(self.driver).move_to_element(guest_btn).click().perform()
                logger.info("Guest clicked via ActionChains")
            except Exception:
                self.driver.execute_script("arguments[0].click();", guest_btn)
                logger.info("Guest clicked via JavaScript")
            screenshot_on_success(self.driver, "guest_selected")
            return True
        except Exception as e:
            logger.error(f"Continue as Guest failed: {e}")
            screenshot_on_failure(self.driver, "guest_fail")
            return False

    # ── Fill Address ───────────────────────────────────────────────
    @allure.step("Fill shipping address")
    def fill_shipping_address(self, pincode="531001"):
        logger.info("Filling shipping address")
        try:
            self._fill_field("//input[@placeholder='Pincode']", pincode)
            logger.info("Pincode entered - waiting 10s for city/state API")
            time.sleep(10)
            self._fill_field(
                "//input[@placeholder='House/ Flat/ Office No.']",
                "Flat 404, Tech Park")
            self._fill_field(
                "//textarea[@placeholder='Road Name/ Area /Colony']",
                "Main Automation Road, Software Layout")
            self._fill_field("//input[@placeholder='Name']", "Test User")
            self._fill_field("//input[@placeholder='Phone']", "9876543210")
            self._fill_field("//input[@placeholder='Email']", "test@example.com")
            time.sleep(2)

            for xpath in SHIP_ADDRESS_XPATHS:
                try:
                    btn = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, xpath)))
                    if btn.is_displayed():
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});", btn)
                        time.sleep(1)
                        try:
                            ActionChains(self.driver).move_to_element(btn).click().perform()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", btn)
                        logger.info("Ship to address clicked")
                        screenshot_on_success(self.driver, "address_filled")
                        return True
                except Exception:
                    continue
            logger.error("Ship to address button not found")
            return False
        except Exception as e:
            logger.error(f"Address fill failed: {e}")
            screenshot_on_failure(self.driver, "address_fail")
            return False

    def _fill_field(self, xpath, text):
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.5)
            try:
                el.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", el)
            el.clear()
            time.sleep(0.5)
            el.send_keys(text)
            logger.info(f"Field filled: {text}")
        except Exception as e:
            logger.error(f"Fill field failed: {e}")

    # ── Helpers ────────────────────────────────────────────────────
    def get_current_url(self):
        return self.driver.current_url

    def get_page_title(self):
        return self.driver.title

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text.lower()

    def is_out_of_stock(self):
        return "OUT OF STOCK" in self.driver.find_element(
            By.TAG_NAME, "body").text.upper()