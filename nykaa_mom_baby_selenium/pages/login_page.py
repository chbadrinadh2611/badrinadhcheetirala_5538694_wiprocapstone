from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def click_login_icon(self):
        try:
            xpaths = [
                "//a[contains(@href,'login')]",
                "//span[contains(text(),'Sign In')]",
                "//a[contains(text(),'Sign In')]",
                "//li[contains(@class,'user')]//a",
                "//div[contains(@class,'user')]//a",
            ]
            for xpath in xpaths:
                try:
                    el = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    el.click()
                    print("[LOGIN] Clicked login icon")
                    time.sleep(3)
                    return
                except Exception:
                    continue
            print("[LOGIN] Login icon not found")
        except Exception as e:
            print("[LOGIN] Error: " + str(e))

    def enter_phone_number(self, phone):
        try:
            # Exact placeholder from screenshot: "Mobile Number"
            xpaths = [
                "//input[@placeholder='Mobile Number']",
                "//input[contains(@placeholder,'Mobile')]",
                "//input[@type='tel']",
                "//input[@type='number']",
                "//input[@maxlength='10']",
            ]
            for xpath in xpaths:
                try:
                    el = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, xpath))
                    )
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(0.5)
                    el.clear()
                    el.send_keys(phone)
                    print("[LOGIN] Phone entered: " + phone)
                    time.sleep(1)
                    return
                except Exception:
                    continue
            # Fallback - try all visible inputs
            inputs = self.driver.find_elements(By.XPATH, "//input")
            for inp in inputs:
                try:
                    if inp.is_displayed():
                        self.driver.execute_script("arguments[0].click();", inp)
                        inp.clear()
                        inp.send_keys(phone)
                        print("[LOGIN] Phone entered via fallback")
                        time.sleep(1)
                        return
                except Exception:
                    continue
        except Exception as e:
            print("[LOGIN] enter_phone error: " + str(e))

    def click_send_otp(self):
        def click_send_otp(self):
            try:
                xpaths = [
                    "//button[text()='Get OTP']",
                    "//button[contains(text(),'Get OTP')]",
                    "//button[contains(text(),'GET OTP')]",
                    "//button[text()='Send OTP']",
                    "//button[contains(text(),'Send OTP')]",
                    "//button[contains(text(),'SEND OTP')]",
                    "//button[@type='submit']",
                ]
                for xpath in xpaths:
                    try:
                        el = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        self.driver.execute_script("arguments[0].click();", el)
                        print("[LOGIN] OTP button clicked: " + xpath)
                        time.sleep(3)
                        return
                    except Exception:
                        continue
                print("[LOGIN] OTP button not found")
            except Exception as e:
                print("[LOGIN] send_otp error: " + str(e))

    def click_verify(self):
        try:
            xpaths = [
                "//button[contains(text(),'Verify')]",
                "//button[contains(text(),'VERIFY')]",
                "//button[contains(text(),'Submit')]",
                "//button[contains(text(),'LOGIN')]",
                "//button[@type='submit']",
            ]
            for xpath in xpaths:
                try:
                    el = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    self.driver.execute_script("arguments[0].click();", el)
                    print("[LOGIN] Verify clicked")
                    time.sleep(3)
                    return
                except Exception:
                    continue
        except Exception as e:
            print("[LOGIN] verify error: " + str(e))

    def is_element_present(self, by, value, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    def is_logged_in(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Hi,')]"))
            )
            return True
        except Exception:
            return False