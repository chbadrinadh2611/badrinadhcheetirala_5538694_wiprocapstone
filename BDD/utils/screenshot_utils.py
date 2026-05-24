import os
import time
import allure
from utils.logger import get_logger

logger = get_logger("Screenshot")

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")


def _ensure_dir():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def _filename(label):
    ts = time.strftime("%Y%m%d_%H%M%S")
    safe = label.replace(" ", "_").replace("/", "-")
    return os.path.join(SCREENSHOT_DIR, f"{safe}_{ts}.png")


def take_screenshot(driver, label="screenshot"):
    _ensure_dir()
    path = _filename(label)
    driver.save_screenshot(path)
    logger.info(f"Screenshot saved: {path}")
    # Attach to Allure
    with open(path, "rb") as f:
        allure.attach(f.read(), name=label, attachment_type=allure.attachment_type.PNG)
    return path


def screenshot_before_click(driver, label="before_click"):
    logger.info(f"Screenshot BEFORE click: {label}")
    return take_screenshot(driver, f"before_click_{label}")


def screenshot_after_click(driver, label="after_click"):
    logger.info(f"Screenshot AFTER click: {label}")
    return take_screenshot(driver, f"after_click_{label}")


def screenshot_on_failure(driver, label="failure"):
    logger.error(f"Screenshot ON FAILURE: {label}")
    return take_screenshot(driver, f"FAILURE_{label}")


def screenshot_on_success(driver, label="success"):
    logger.info(f"Screenshot ON SUCCESS: {label}")
    return take_screenshot(driver, f"SUCCESS_{label}")
