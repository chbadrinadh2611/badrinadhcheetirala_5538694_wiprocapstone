import pytest
import os
import subprocess
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# ══════════════════════════════════════════════════════════════════════
# CONFIGURATION & DRIVER FIXTURES
# ══════════════════════════════════════════════════════════════════════

def read_config():
    config = {}
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.properties")
    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("["):
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    return config


@pytest.fixture(scope="session")
def config():
    return read_config()


@pytest.fixture(scope="function")
def driver(config):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", False)

    driver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    yield driver

    try:
        driver.close()
    except Exception:
        pass
    try:
        driver.quit()
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════════
# AUTOMATIC NATIVE ALLURE SINGLE FILE GENERATION HOOK
# ══════════════════════════════════════════════════════════════════════

def pytest_sessionfinish(session, exitstatus):
    """
    This hook runs automatically after the test run finishes.
    It compiles raw Allure data straight into a standalone, single HTML file
    using Allure's native single-file compiler.
    """
    print("\n🏁 Test run complete. Processing reports in terminal...")

    results_dir = os.path.abspath(os.path.join("reports", "allure-results"))
    report_dir = os.path.abspath(os.path.join("reports", "allure-report"))

    if os.path.exists(results_dir):
        try:
            allure_bin = shutil.which("allure") or "allure"
            print("📦 Compiling native single-file dashboard into reports/allure-report...")

            # The --single-file flag tells Allure to pack everything directly into index.html natively
            gen_cmd = f'"{allure_bin}" generate "{results_dir}" --clean --single-file -o "{report_dir}"'
            subprocess.run(gen_cmd, shell=True, check=True)

            print("\n🎉 SUCCESS: Standalone Allure Report generated cleanly!")
            print(f"👉 Path to view: reports\\allure-report\\index.html")

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Native single-file compilation failed: {e}")
        except Exception as e:
            print(f"\n❌ An error occurred during automatic reporting layout: {e}")
    else:
        print(f"\n⚠️ Missing data directory: '{results_dir}'.")