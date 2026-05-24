from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time


class ProductPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_title(self):
        try:
            el = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//h1"))
            )
            return el.text
        except Exception:
            return "Unknown Product"

    def is_out_of_stock(self):
        try:
            text = self.driver.find_element(
                By.XPATH, "//body").text.upper()
            return "OUT OF STOCK" in text
        except Exception:
            return False

    def click_add_to_bag(self):
        try:
            time.sleep(3)
            # Use JavaScript to find and click ADD TO BAG button
            result = self.driver.execute_script("""
                var els = document.querySelectorAll('button,div,span,a');
                for(var i=0; i<els.length; i++){
                    var t = els[i].innerText;
                    if(t && (t.trim() === 'ADD TO BAG' ||
                             t.trim() === 'Add to Bag' ||
                             t.trim() === 'ADD TO CART' ||
                             t.trim() === 'Add to Cart')){
                        els[i].click();
                        return 'clicked: ' + t.trim();
                    }
                }
                return 'not found';
            """)
            print("[PRODUCT] Add to bag result: " + str(result))
            time.sleep(3)
        except Exception as e:
            print("[PRODUCT] Add to bag error: " + str(e))

    def click_go_to_bag(self):
        """
        After clicking Add to Bag, a side panel opens.
        We need to click the bag icon at top right
        OR click the Proceed button inside the side panel.
        """
        try:
            time.sleep(2)

            # First try clicking Proceed button in side panel
            proceed_xpaths = [
                "//button[contains(text(),'Proceed')]",
                "//a[contains(text(),'Proceed')]",
                "//button[contains(text(),'PROCEED')]",
                "//div[contains(text(),'Proceed')]",
                "//*[contains(@class,'proceed')]",
            ]
            for xpath in proceed_xpaths:
                try:
                    el = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, xpath))
                    )
                    self.driver.execute_script(
                        "arguments[0].click();", el)
                    print("[PRODUCT] Proceed clicked in side panel")
                    time.sleep(3)
                    return
                except Exception:
                    continue

            # Try clicking GO TO BAG text
            go_bag_xpaths = [
                "//*[contains(text(),'GO TO BAG')]",
                "//*[contains(text(),'Go to Bag')]",
                "//*[contains(text(),'VIEW BAG')]",
                "//*[contains(text(),'View Bag')]",
            ]
            for xpath in go_bag_xpaths:
                try:
                    el = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, xpath))
                    )
                    self.driver.execute_script(
                        "arguments[0].click();", el)
                    print("[PRODUCT] Go to bag clicked")
                    time.sleep(3)
                    return
                except Exception:
                    continue

            # Try clicking bag icon at top right
            bag_icon_xpaths = [
                "//a[contains(@href,'bag')]",
                "//a[contains(@href,'cart')]",
                "//*[contains(@class,'bag')]//a",
                "//*[contains(@aria-label,'bag')]",
                "//*[contains(@aria-label,'cart')]",
            ]
            for xpath in bag_icon_xpaths:
                try:
                    el = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, xpath))
                    )
                    self.driver.execute_script(
                        "arguments[0].click();", el)
                    print("[PRODUCT] Bag icon clicked")
                    time.sleep(3)
                    return
                except Exception:
                    continue

            # Last resort - navigate directly
            print("[PRODUCT] Navigating directly to bag")
            self.driver.get("https://www.nykaa.com/bag")
            time.sleep(3)

        except Exception as e:
            print("[PRODUCT] Go to bag error: " + str(e))
            self.driver.get("https://www.nykaa.com/bag")
            time.sleep(3)

    def click_proceed_to_checkout(self):
        """Click Proceed button on bag page to go to checkout"""
        try:
            time.sleep(2)
            proceed_xpaths = [
                "//button[contains(text(),'Proceed')]",
                "//a[contains(text(),'Proceed')]",
                "//button[contains(text(),'PROCEED')]",
            ]
            for xpath in proceed_xpaths:
                try:
                    el = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, xpath))
                    )
                    self.driver.execute_script(
                        "arguments[0].click();", el)
                    print("[PRODUCT] Proceed to checkout clicked")
                    time.sleep(4)
                    return True
                except Exception:
                    continue
            return False
        except Exception as e:
            print("[PRODUCT] Proceed error: " + str(e))
            return False

    def get_product_price(self):
        try:
            el = self.driver.find_element(
                By.XPATH, "//*[contains(text(),'₹')]")
            return el.text
        except Exception:
            return "Price not found"