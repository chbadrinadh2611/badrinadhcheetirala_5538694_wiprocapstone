import pytest
import time
import logging
import os
import allure

from datetime import datetime
from allure_commons.types import AttachmentType

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ══════════════════════════════════════════════════════════════════════
# LOGGING SETUP
# ══════════════════════════════════════════════════════════════════════

os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/execution.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════

BABY_CARE_URL = "https://www.nykaa.com/baby-care/c/14798"

BRAND_FILTER_DATA = [
    pytest.param("Mamaearth", id="brand_Mamaearth"),
    pytest.param("Himalaya", id="brand_Himalaya"),
    pytest.param("Cetaphil", id="brand_Cetaphil"),
]

DISCOUNT_FILTER_DATA = [
    pytest.param("10% And Above", id="discount_10"),
    pytest.param("20% And Above", id="discount_20"),
]

INVALID_BRAND_DATA = [
    pytest.param("XYZ123InvalidBrand", id="invalid_XYZ123"),
    pytest.param("NoSuchBrandABC", id="invalid_ABC"),
]

# ══════════════════════════════════════════════════════════════════════
# SCREENSHOT FUNCTION WITH ALLURE
# ══════════════════════════════════════════════════════════════════════

def safe_screenshot(driver, name):

    try:

        os.makedirs("screenshots", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        path = f"screenshots/{name}_{timestamp}.png"

        driver.save_screenshot(path)

        allure.attach.file(
            path,
            name=name,
            attachment_type=AttachmentType.PNG
        )

        log.info(f"Screenshot saved and attached to Allure: {path}")

    except Exception as e:

        log.warning(f"Screenshot failed: {e}")

# ══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def open_baby_care(driver):

    driver.get(BABY_CARE_URL)

    time.sleep(4)

    assert "baby-care" in driver.current_url, \
        "Baby care URL not loaded properly"

    assert "Nykaa" in driver.title, \
        "Nykaa title missing"

    log.info("Baby Care page opened successfully")


def get_product_count(driver):

    time.sleep(2)

    items = driver.find_elements(
        By.XPATH,
        "//a[contains(@href,'/p/')]"
    )

    log.info(f"Product count on page: {len(items)}")

    return len(items)


def expand_filter(driver, filter_name):

    try:

        el = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                f"//div[normalize-space(text())='{filter_name}'] | "
                f"//p[normalize-space(text())='{filter_name}'] | "
                f"//span[normalize-space(text())='{filter_name}']"
            ))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            el
        )

        time.sleep(1)

        driver.execute_script(
            "arguments[0].click();",
            el
        )

        time.sleep(2)

        log.info(f"Filter section expanded: {filter_name}")

        return True

    except Exception as e:

        log.error(f"Could not expand filter '{filter_name}': {e}")

        return False


def click_filter_option(driver, option):

    try:

        el = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                f"//label[contains(text(),'{option}')] | "
                f"//span[contains(text(),'{option}')] | "
                f"//div[contains(text(),'{option}')]"
            ))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            el
        )

        time.sleep(1)

        driver.execute_script(
            "arguments[0].click();",
            el
        )

        time.sleep(4)

        log.info(f"Filter option selected: {option}")

        return True

    except Exception as e:

        log.error(f"Could not click filter option '{option}': {e}")

        return False


def apply_sort(driver, sort_text):

    try:

        sort_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                "//div[contains(text(),'Sort By')] | "
                "//div[contains(text(),'Sort by')] | "
                "//span[contains(text(),'Sort By')]"
            ))
        )

        driver.execute_script("arguments[0].click();", sort_btn)

        time.sleep(2)

        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                f"//li[contains(text(),'{sort_text}')] | "
                f"//div[contains(text(),'{sort_text}')] | "
                f"//span[contains(text(),'{sort_text}')]"
            ))
        )

        driver.execute_script("arguments[0].click();", option)

        time.sleep(4)

        log.info(f"Sort applied: {sort_text}")

        return True

    except Exception as e:

        log.error(f"Sort failed '{sort_text}': {e}")

        return False


# ══════════════════════════════════════════════════════════════════════
# POSITIVE TEST CASES
# ══════════════════════════════════════════════════════════════════════

class TestPositiveCases:

    @pytest.mark.parametrize("brand", BRAND_FILTER_DATA)
    def test_TC_01_brand_filter(self, driver, brand):

        log.info("=" * 55)
        log.info(f"TC_01 STARTED - Brand Filter: {brand}")
        log.info("=" * 55)

        open_baby_care(driver)

        count_before = get_product_count(driver)

        safe_screenshot(driver, f"TC_01_{brand}_page_opened")

        assert count_before > 0, \
            "No products loaded before applying brand filter"

        assert driver.current_url.startswith("https"), \
            "Website is not secured with HTTPS"

        driver.execute_script("window.scrollTo(0, 300)")

        time.sleep(2)

        expanded = expand_filter(driver, "Brand")

        assert expanded, \
            "Brand filter section could not be expanded"

        safe_screenshot(driver, f"TC_01_{brand}_filter_expanded")

        clicked = click_filter_option(driver, brand)

        safe_screenshot(driver, f"TC_01_{brand}_selected")

        assert clicked, \
            f"Brand filter '{brand}' was not selected"

        count_after = get_product_count(driver)

        safe_screenshot(driver, f"TC_01_{brand}_result")

        assert count_after > 0, \
            f"No products displayed after selecting {brand}"

        assert count_after <= count_before, \
            "Filtered product count is unexpectedly greater"

        assert driver.execute_script(
            "return document.readyState"
        ) == "complete", \
            "Page not fully loaded"

        log.info(f"TC_01 PASSED - {brand}")

    @pytest.mark.parametrize("discount", DISCOUNT_FILTER_DATA)
    def test_TC_02_discount_filter(self, driver, discount):

        log.info("=" * 55)
        log.info(f"TC_02 STARTED - Discount Filter: {discount}")
        log.info("=" * 55)

        open_baby_care(driver)

        count_before = get_product_count(driver)

        safe_screenshot(driver, f"TC_02_{discount}_page_opened")

        assert count_before > 0, \
            "Products not loaded before applying discount filter"

        driver.execute_script("window.scrollTo(0, 300)")

        time.sleep(2)

        expanded = expand_filter(driver, "Discount")

        assert expanded, \
            "Discount filter section could not be expanded"

        clicked = click_filter_option(driver, discount)

        if not clicked:

            clicked = click_filter_option(driver, discount.lower())

        safe_screenshot(driver, f"TC_02_{discount}_selected")

        assert clicked, \
            f"Discount option '{discount}' not selectable"

        count_after = get_product_count(driver)

        safe_screenshot(driver, f"TC_02_{discount}_result")

        assert count_after > 0, \
            "No products displayed after discount selection"

        assert count_after <= count_before, \
            "Discount filter did not reduce/refine products"

        log.info(f"TC_02 PASSED - {discount}")

    def test_TC_03_three_filters_proceed_to_payment(self, driver):

        log.info("=" * 55)
        log.info("TC_03 STARTED - End To End Flow")
        log.info("=" * 55)

        open_baby_care(driver)

        safe_screenshot(driver, "TC_03_page_opened")

        driver.execute_script("window.scrollTo(0, 300)")

        time.sleep(2)

        assert expand_filter(driver, "Brand"), \
            "Brand filter could not be expanded"

        assert click_filter_option(driver, "Mamaearth"), \
            "Mamaearth brand selection failed"

        safe_screenshot(driver, "TC_03_brand_selected")

        assert expand_filter(driver, "Discount"), \
            "Discount filter could not be expanded"

        discount_clicked = click_filter_option(
            driver,
            "10% And Above"
        )

        if not discount_clicked:

            discount_clicked = click_filter_option(
                driver,
                "10% and above"
            )

        assert discount_clicked, \
            "Discount filter selection failed"

        safe_screenshot(driver, "TC_03_discount_selected")

        sorted_applied = apply_sort(driver, "Popularity")

        assert sorted_applied, \
            "Sort by Popularity failed"

        safe_screenshot(driver, "TC_03_sort_applied")

        count = get_product_count(driver)

        assert count > 0, \
            "No products displayed after applying all filters"

        products = driver.find_elements(
            By.XPATH,
            "//a[contains(@href,'/p/')]"
        )

        assert len(products) > 0, \
            "Product links not found"

        first_url = products[0].get_attribute("href")

        assert first_url is not None, \
            "First product URL is empty"

        assert "/p/" in first_url, \
            "Product URL format invalid"

        driver.get(first_url)

        time.sleep(4)

        safe_screenshot(driver, "TC_03_product_page")

        assert "/p/" in driver.current_url, \
            "Product detail page not opened"

        body = driver.find_element(By.XPATH, "//body").text.upper()

        assert "ADD TO BAG" in body or "ADD TO CART" in body, \
            "Add to Bag button text not present"

        log.info("TC_03 PASSED - End To End Flow successful")

# ══════════════════════════════════════════════════════════════════════
# NEGATIVE TEST CASES
# ══════════════════════════════════════════════════════════════════════

class TestNegativeCases:

    @pytest.mark.parametrize("invalid_brand", INVALID_BRAND_DATA)
    def test_TC_04_invalid_brand_search(self, driver, invalid_brand):

        log.info("=" * 55)
        log.info(f"TC_04 STARTED - Invalid Brand: {invalid_brand}")
        log.info("=" * 55)

        open_baby_care(driver)

        driver.execute_script("window.scrollTo(0, 300)")

        time.sleep(2)

        expanded = expand_filter(driver, "Brand")

        assert expanded, \
            "Brand filter section expansion failed"

        body_text = driver.find_element(
            By.XPATH,
            "//body"
        ).text.lower()

        safe_screenshot(driver, f"TC_04_{invalid_brand}")

        assert invalid_brand.lower() not in body_text, \
            f"Invalid brand '{invalid_brand}' unexpectedly found"

        log.info(f"TC_04 PASSED - {invalid_brand}")

    def test_TC_05_invalid_filter_rejection(self, driver):

        log.info("=" * 55)
        log.info("TC_05 STARTED - Invalid Discount Validation")
        log.info("=" * 55)

        open_baby_care(driver)

        driver.execute_script("window.scrollTo(0, 300)")

        time.sleep(2)

        expanded = expand_filter(driver, "Discount")

        assert expanded, \
            "Discount filter section expansion failed"

        clicked = click_filter_option(
            driver,
            "150% And Above"
        )

        safe_screenshot(driver, "TC_05_invalid_discount")

        assert clicked is False or clicked is None, \
            "Invalid discount filter unexpectedly exists"

        log.info("TC_05 PASSED - Invalid discount correctly absent")