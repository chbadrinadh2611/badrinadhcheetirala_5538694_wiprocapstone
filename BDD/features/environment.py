import os
import sys
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.logger import get_logger
from utils.screenshot_utils import screenshot_on_failure, screenshot_on_success

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

logger = get_logger("Environment")

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "execution.log")
DRIVER_PATH = r"C:\Users\user\.wdm\drivers\chromedriver\win64\148.0.7778.178\chromedriver-win64\chromedriver.exe"


def attach_logs_to_allure():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                allure.attach(
                    f.read(),
                    name="Execution Log",
                    attachment_type=allure.attachment_type.TEXT
                )
            logger.info("Logs attached to Allure")
    except Exception as e:
        logger.warning(f"Log attach failed: {e}")


def before_all(context):
    logger.info("=" * 60)
    logger.info("BDD TEST SUITE STARTED")
    logger.info("=" * 60)


def before_scenario(context, scenario):
    logger.info(f"--- Scenario START: {scenario.name} ---")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--start-maximized")

        service = Service(DRIVER_PATH)
        context.driver = webdriver.Chrome(service=service, options=options)
        context.driver.implicitly_wait(5)
        logger.info("Chrome driver initialized successfully")

    except Exception as e:
        logger.error(f"Driver init failed: {e}")
        raise


def after_step(context, step):
    if step.status == "failed":
        logger.error(f"Step FAILED: {step.name}")
        try:
            screenshot_on_failure(context.driver, step.name[:50])
        except Exception as e:
            logger.warning(f"Screenshot skipped: {e}")
    else:
        logger.info(f"Step PASSED: {step.name}")


def after_scenario(context, scenario):
    status = scenario.status
    logger.info(f"--- Scenario END: {scenario.name} | Status: {status} ---")

    # Attach logs to allure after every scenario
    attach_logs_to_allure()

    if status == "passed":
        try:
            screenshot_on_success(context.driver, "scenario_passed")
        except Exception:
            pass
    try:
        context.driver.quit()
        logger.info("Driver closed")
    except Exception as e:
        logger.warning(f"Driver quit error: {e}")


def after_all(context):
    logger.info("=" * 60)
    logger.info("BDD TEST SUITE COMPLETED")
    logger.info("=" * 60)

    # Attach final full log to allure
    attach_logs_to_allure()