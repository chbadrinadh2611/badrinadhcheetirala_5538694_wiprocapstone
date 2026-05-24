import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import allure
from behave import when, then
from selenium.webdriver.common.by import By
from pages.nykaa_page import NykaaPage
from utils.logger import get_logger
from utils.screenshot_utils import screenshot_on_success

logger = get_logger("E2ESteps")


@when("I click on the first product")
@allure.step("Click first product")
def step_click_first_product(context):
    logger.info("[STEP] When: Click first product")
    if not hasattr(context, "nykaa"):
        context.nykaa = NykaaPage(context.driver)
    context.nykaa.click_first_product()


@when("I check product is not out of stock")
@allure.step("Check stock status")
def step_check_stock(context):
    logger.info("[STEP] When: Check stock")
    if context.nykaa.is_out_of_stock():
        logger.warning("Product is out of stock - skipping")
        context.scenario.skip("Product out of stock")


@when("I add the product to the bag")
@allure.step("Add to bag")
def step_add_to_bag(context):
    logger.info("[STEP] When: Add to bag")
    result = context.nykaa.add_to_bag()
    assert result, "Add to Bag failed"


@then("the cart should reflect the added item")
@allure.step("Validate cart")
def step_validate_cart(context):
    logger.info("[STEP] Then: Validate cart")
    body = context.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "bag" in body or "cart" in body, "Cart not updated"
    screenshot_on_success(context.driver, "cart_validated")
    logger.info("PASSED: Cart updated")


@when("I proceed to checkout")
@allure.step("Proceed to checkout")
def step_proceed(context):
    logger.info("[STEP] When: Proceed to checkout")
    context.driver.execute_script("window.scrollTo(0, 0);")
    import time
    time.sleep(1)
    result = context.nykaa.open_bag()
    assert result, "Bag icon not found"
    result = context.nykaa.click_proceed()
    assert result, "Proceed button not found"


@when("I continue as guest")
@allure.step("Continue as guest")
def step_guest(context):
    logger.info("[STEP] When: Continue as guest")
    result = context.nykaa.continue_as_guest()
    assert result, "Continue as Guest failed"


@when("I fill the shipping address")
@allure.step("Fill shipping address")
def step_fill_address(context):
    logger.info("[STEP] When: Fill shipping address")
    result = context.nykaa.fill_shipping_address(pincode="531001")
    assert result, "Address fill failed"


@then("the checkout page should be displayed")
@allure.step("Validate checkout page")
def step_validate_checkout(context):
    logger.info("[STEP] Then: Validate checkout page")
    import time
    time.sleep(10)
    url = context.driver.current_url.lower()
    body = context.driver.find_element(By.TAG_NAME, "body").text.lower()
    reached = (
        "payment" in url or "checkout" in url or
        "address" in url or "payment" in body or "pay" in body
    )
    assert reached, "Did not reach checkout/payment page"
    screenshot_on_success(context.driver, "checkout_reached")
    logger.info("PASSED: Checkout page reached")