import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import allure
from behave import given, when, then
from pages.nykaa_page import NykaaPage
from utils.logger import get_logger
from utils.screenshot_utils import screenshot_on_success

logger = get_logger("PositiveSteps")


@given("I open the Nykaa Baby Care page")
@allure.step("Open Nykaa Baby Care page")
def step_open_nykaa(context):
    logger.info("[STEP] Given: Open Nykaa Baby Care page")
    context.nykaa = NykaaPage(context.driver)
    context.nykaa.open_page()


@when("I expand the Brand filter")
@allure.step("Expand Brand filter")
def step_expand_brand(context):
    logger.info("[STEP] When: Expand Brand filter")
    result = context.nykaa.expand_filter("Brand")
    assert result, "Brand filter expansion failed"


@when("I expand the Avg Customer Rating filter")
@allure.step("Expand Rating filter")
def step_expand_rating(context):
    logger.info("[STEP] When: Expand Rating filter")
    result = context.nykaa.expand_filter("Avg Customer Rating")
    assert result, "Rating filter expansion failed"


@when("I expand the Discount filter")
@allure.step("Expand Discount filter")
def step_expand_discount(context):
    logger.info("[STEP] When: Expand Discount filter")
    result = context.nykaa.expand_filter("Discount")
    assert result, "Discount filter expansion failed"


@when('I select the brand "{brand}"')
@allure.step("Select brand")
def step_select_brand(context, brand):
    logger.info(f"[STEP] When: Select brand '{brand}'")
    result = context.nykaa.click_filter_option(brand)
    assert result, f"Brand selection failed: {brand}"


@when('I select the rating "{rating}"')
@allure.step("Select rating")
def step_select_rating(context, rating):
    logger.info(f"[STEP] When: Select rating '{rating}'")
    result = context.nykaa.click_filter_option(rating)
    assert result, f"Rating selection failed: {rating}"


@when('I select the discount "{discount}"')
@allure.step("Select discount")
def step_select_discount(context, discount):
    logger.info(f"[STEP] When: Select discount '{discount}'")
    result = context.nykaa.click_filter_option(discount)
    if not result:
        result = context.nykaa.click_filter_option(discount.lower())
    assert result, f"Discount selection failed: {discount}"


@then("products should be displayed on the page")
@allure.step("Validate products displayed")
def step_validate_products(context):
    logger.info("[STEP] Then: Validate products displayed")
    products = context.nykaa.get_products()
    assert len(products) > 0, f"No products found"
    logger.info(f"PASSED: {len(products)} products found")
    screenshot_on_success(context.driver, "products_validated")


@then('the URL should contain "{keyword}"')
@allure.step("Validate URL")
def step_validate_url(context, keyword):
    logger.info(f"[STEP] Then: URL should contain '{keyword}'")
    url = context.nykaa.get_current_url()
    assert keyword in url, f"'{keyword}' not in URL: {url}"
    logger.info(f"PASSED: URL contains '{keyword}'")


@then("the page title should not be empty")
@allure.step("Validate page title")
def step_validate_title(context):
    logger.info("[STEP] Then: Page title should not be empty")
    title = context.nykaa.get_page_title()
    assert len(title) > 0, "Page title is empty"
    logger.info(f"PASSED: Title = '{title}'")


@then("the product count should be greater than 0")
@allure.step("Validate product count")
def step_validate_count(context):
    logger.info("[STEP] Then: Product count > 0")
    products = context.nykaa.get_products()
    assert len(products) > 0, f"Product count is {len(products)}"
    logger.info(f"PASSED: Count = {len(products)}")