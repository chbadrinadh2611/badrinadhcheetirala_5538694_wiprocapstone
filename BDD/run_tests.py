import os
import sys
import shutil
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
ALLURE_RESULTS  = os.path.join(ROOT, "reports", "allure-results")
ALLURE_REPORT   = os.path.join(ROOT, "reports", "allure-report")
SCREENSHOTS_DIR = os.path.join(ROOT, "reports", "screenshots")
LOGS_DIR        = os.path.join(ROOT, "logs")

# Full path to allure CLI
ALLURE_CMD = r"C:\Users\user\Downloads\allure-2.41.0\allure-2.41.0\bin\allure.bat"


def clean_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    print(f"[CLEAN] Cleaned: {path}")


def allure_cli_available():
    return os.path.exists(ALLURE_CMD)


def run_behave():
    print("\n" + "=" * 60)
    print("  RUNNING BEHAVE BDD TESTS")
    print("=" * 60)
    cmd = [
        sys.executable, "-m", "behave",
        "--no-capture",
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", ALLURE_RESULTS,
        "-f", "pretty",
    ]
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


def generate_allure_report():
    print("\n" + "=" * 60)
    print("  GENERATING ALLURE REPORT")
    print("=" * 60)
    if not allure_cli_available():
        print(f"[WARN] Allure not found at: {ALLURE_CMD}")
        return 1
    result = subprocess.run(
        [ALLURE_CMD, "generate", ALLURE_RESULTS, "--clean", "-o", ALLURE_REPORT],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"[OK] Report generated: {ALLURE_REPORT}")
    else:
        print(f"[WARN] {result.stderr}")
    return result.returncode


def open_allure_report():
    print("\n" + "=" * 60)
    print("  OPENING ALLURE REPORT AUTOMATICALLY")
    print("=" * 60)
    if not allure_cli_available():
        print(f"[WARN] Allure not found at: {ALLURE_CMD}")
        return
    try:
        print("[OK] Opening Allure report in browser...")
        print("[INFO] Press Ctrl+C to stop the server when done.")
        subprocess.run([ALLURE_CMD, "serve", ALLURE_RESULTS])
    except KeyboardInterrupt:
        print("\n[INFO] Allure server stopped.")
    except Exception as e:
        print(f"[WARN] Could not open report: {e}")


def main():
    print("\n" + "=" * 60)
    print("  NYKAA BDD AUTOMATION FRAMEWORK")
    print("=" * 60)

    print("\n[1/4] Cleaning previous results...")
    clean_directory(ALLURE_RESULTS)
    clean_directory(SCREENSHOTS_DIR)
    os.makedirs(LOGS_DIR, exist_ok=True)

    print("\n[2/4] Executing Behave tests...")
    exit_code = run_behave()

    print("\n[3/4] Generating Allure report...")
    generate_allure_report()

    print("\n[4/4] Opening Allure report automatically...")
    open_allure_report()

    print("\n" + "=" * 60)
    print(f"  EXECUTION COMPLETE | Exit Code: {exit_code}")
    print("=" * 60)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())