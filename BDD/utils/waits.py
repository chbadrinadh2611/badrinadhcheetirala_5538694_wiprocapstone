import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from utils.logger import get_logger

logger = get_logger("Waits")

DEFAULT_TIMEOUT = 15
POLL_FREQUENCY = 0.5


def wait_for_element(driver, locator, timeout=DEFAULT_TIMEOUT):
    logger.info(f"Waiting for element: {locator}")
    try:
        element = WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            EC.presence_of_element_located(locator)
        )
        logger.info(f"Element found: {locator}")
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for element: {locator}")
        raise


def wait_for_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    logger.info(f"Waiting for clickable: {locator}")
    try:
        element = WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            EC.element_to_be_clickable(locator)
        )
        logger.info(f"Element clickable: {locator}")
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for clickable element: {locator}")
        raise


def wait_for_elements(driver, locator, timeout=DEFAULT_TIMEOUT):
    logger.info(f"Waiting for multiple elements: {locator}")
    try:
        elements = WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            EC.presence_of_all_elements_located(locator)
        )
        logger.info(f"Found {len(elements)} elements for: {locator}")
        return elements
    except TimeoutException:
        logger.error(f"Timeout waiting for elements: {locator}")
        raise


def retry_click(driver, locator, retries=3, delay=1):
    logger.info(f"Retry click on: {locator}")
    for attempt in range(1, retries + 1):
        try:
            element = wait_for_clickable(driver, locator)
            scroll_into_view(driver, element)
            js_click(driver, element)
            logger.info(f"Retry click succeeded on attempt {attempt}")
            return element
        except (StaleElementReferenceException, Exception) as e:
            logger.warning(f"Retry {attempt} failed: {e}")
            time.sleep(delay)
    raise Exception(f"All {retries} retry attempts failed for: {locator}")


def scroll_into_view(driver, element):
    logger.info("Scrolling element into view")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    time.sleep(0.3)


def js_click(driver, element):
    logger.info("Performing JavaScript click")
    driver.execute_script("arguments[0].click();", element)


def short_sleep(seconds=1):
    logger.info(f"Short sleep: {seconds}s")
    time.sleep(seconds)
