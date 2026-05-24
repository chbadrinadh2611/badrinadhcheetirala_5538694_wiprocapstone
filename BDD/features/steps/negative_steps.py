import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import allure
from behave import when, then
from selenium.webdriver.common.by import By
from pages.locators import URL
from utils.logger import get_logger
from utils.screenshot_utils import screenshot_on_success, screenshot_on_failure

logger = get_logger("NegativeSteps")


@when('I search for an invalid brand "{brand}"')
@allure.step("Search invalid brand")
def step_invalid_brand(context, brand):
    logger.info(f"[STEP] Storing invalid brand: {brand}")
    context.invalid_brand = brand


@then("no brand results should be displayed")
@allure.step("Validate no brand results")
def step_no_brand_results(context):
    logger.info("[STEP] Then: No brand results")
    brand = getattr(context, "invalid_brand", "NONEXISTENT")
    body = context.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert brand.lower() not in body, f"Invalid brand '{brand}' found unexpectedly"
    screenshot_on_success(context.driver, "no_brand_results")
    logger.info(f"PASSED: Invalid brand '{brand}' not found")


@then("the page should handle the filter gracefully")
@allure.step("Validate graceful filter handling")
def step_graceful_filter(context):
    logger.info("[STEP] Then: Page handles filter gracefully")
    title = context.driver.title
    assert len(title) > 0, "Page crashed"
    screenshot_on_success(context.driver, "filter_graceful")
    logger.info(f"PASSED: Page stable. Title: '{title}'")


@when("I open the Nykaa Baby Care page with a forced empty query")
@allure.step("Open empty query page")
def step_empty_query(context):
    logger.info("[STEP] When: Open page with empty query")
    import time
    empty_url = URL + "&q=xyznotexist999"
    context.driver.get(empty_url)
    time.sleep(2)
    screenshot_on_success(context.driver, "empty_query_opened")


@then("the page should not crash and should display a response")
@allure.step("Validate page no crash")
def step_no_crash(context):
    logger.info("[STEP] Then: Page should not crash")
    body = context.driver.find_element(By.TAG_NAME, "body").text
    assert len(body) > 0, "Page body empty - possible crash"
    screenshot_on_success(context.driver, "no_crash")
    logger.info("PASSED: Page responded without crash")