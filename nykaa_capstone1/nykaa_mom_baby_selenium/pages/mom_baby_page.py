from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time


class MomBabyPage(BasePage):

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
            text = self.driver.find_element(By.XPATH, "//body").text
            return "OUT OF STOCK" in text.upper()
        except Exception:
            return False

    def click_add_to_bag(self):
        try:
            time.sleep(3)
            # Try multiple approaches
            # Approach 1 - find by text using JS
            result = self.driver.execute_script("""
                var buttons = document.querySelectorAll('button');
                for(var i=0; i<buttons.length; i++){
                    if(buttons[i].innerText.includes('ADD TO BAG') || 
                       buttons[i].innerText.includes('Add to Bag')){
                        buttons[i].click();
                        return 'clicked:' + buttons[i].innerText;
                    }
                }
                var divs = document.querySelectorAll('div');
                for(var i=0; i<divs.length; i++){
                    if(divs[i].innerText === 'ADD TO BAG' || 
                       divs[i].innerText === 'Add to Bag'){
                        divs[i].click();
                        return 'div clicked:' + divs[i].innerText;
                    }
                }
                return 'not found';
            """)
            print(f"[PRODUCT] JS click result: {result}")
            time.sleep(3)

            if "not found" in str(result):
                # Approach 2 - xpath with wait
                xpaths = [
                    "//*[text()='ADD TO BAG']",
                    "//*[text()='Add to Bag']",
                    "//button[contains(.,'ADD TO BAG')]",
                    "//button[contains(.,'Add to Bag')]",
                    "//*[contains(@class,'add-to-bag')]",
                    "//*[contains(@class,'addToBag')]",
                    "//*[contains(@class,'atb')]",
                ]
                for xpath in xpaths:
                    try:
                        el = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        self.driver.execute_script("arguments[0].click();", el)
                        print(f"[PRODUCT] Clicked via xpath: {xpath}")
                        time.sleep(3)
                        return
                    except Exception:
                        continue
        except Exception as e:
            print(f"[PRODUCT] Add to bag error: {e}")

    def click_go_to_bag(self):
        try:
            time.sleep(2)
            result = self.driver.execute_script("""
                var elements = document.querySelectorAll('button,a,div,span');
                for(var i=0; i<elements.length; i++){
                    var txt = elements[i].innerText;
                    if(txt && (txt.includes('GO TO BAG') || txt.includes('Go to Bag') || 
                       txt.includes('VIEW BAG') || txt.includes('Go To Bag'))){
                        elements[i].click();
                        return 'clicked:' + txt;
                    }
                }
                return 'not found';
            """)
            print(f"[PRODUCT] Go to bag JS result: {result}")
            time.sleep(3)

            if "not found" in str(result):
                print("[PRODUCT] Navigating directly to bag")
                self.driver.get("https://www.nykaa.com/bag")
                time.sleep(3)
        except Exception as e:
            print(f"[PRODUCT] Go to bag error: {e}")
            self.driver.get("https://www.nykaa.com/bag")
            time.sleep(3)

    def get_product_price(self):
        try:
            el = self.driver.find_element(By.XPATH, "//*[contains(text(),'₹')]")
            return el.text
        except Exception:
            return "Price not found"