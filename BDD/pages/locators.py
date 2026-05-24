from selenium.webdriver.common.by import By

URL = "https://www.nykaa.com/mom-baby/baby-care/c/14798?redirectpath=slug"

# Products
PRODUCTS = (By.XPATH, "//a[contains(@href,'/p/')]")

# Add to Bag - multiple fallback xpaths
ADD_TO_BAG_XPATHS = [
    "//button[normalize-space()='Add to Bag']",
    "//button[contains(., 'Add to Bag')]",
    "//span[contains(text(), 'Add to Bag')]/ancestor::button",
    "//button[contains(@class, 'add-to-bag')]"
]

# Bag icon in header - id is most stable
BAG_ICON_XPATHS = [
    "//button[@id='header-bag-icon']",
    "//*[@id='header-bag-icon']",
    "//*[@data-testid='cart-icon']",
    "//*[@data-testid='bag-icon']",
    "//*[contains(@class,'headerCart')]",
]

# Proceed button in sidebar
PROCEED_XPATHS = [
    "//button[@data-test-id='footer-proceed-cta']",
    "//*[@data-test-id='footer-proceed-cta']",
    "//span[@data-test-id='footer-proceed-title']/ancestor::button"
]

# Guest checkout
GUEST_CHECKOUT = (By.XPATH, "//button[@data-testid='button_continueAsGuest']")

# Ship to address
SHIP_ADDRESS_XPATHS = [
    "//button[@data-testid='button_shipToThisAddress']",
    "//*[@data-testid='button_shipToThisAddress']",
    "//button[normalize-space(text())='SHIP TO THIS ADDRESS']"
]

# Address Fields
PINCODE_FIELD = (By.XPATH, "//input[@placeholder='Pincode']")
HOUSE_FIELD   = (By.XPATH, "//input[@placeholder='House/ Flat/ Office No.']")
ROAD_FIELD    = (By.XPATH, "//textarea[@placeholder='Road Name/ Area /Colony']")
NAME_FIELD    = (By.XPATH, "//input[@placeholder='Name']")
PHONE_FIELD   = (By.XPATH, "//input[@placeholder='Phone']")
EMAIL_FIELD   = (By.XPATH, "//input[@placeholder='Email']")