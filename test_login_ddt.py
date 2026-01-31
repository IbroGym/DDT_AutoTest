import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from excel_reader import load_login_cases


LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"


def get_actual_outcome(driver, wait) -> str:

    # Success: URL contains this + Log out button is visible
    if "logged-in-successfully" in driver.current_url:
        return "success"

    # Negative: error message is shown on login page
    try:
        error = wait.until(EC.visibility_of_element_located((By.ID, "error")))
        msg = error.text.lower()
        # Common message: "Your username is invalid!" or "Your password is invalid!"
        if "username" in msg and "invalid" in msg:
            return "invalid_username"
        if "password" in msg and "invalid" in msg:
            return "invalid_password"
        return "unknown_error"
    except TimeoutException:
        return "unknown_error"


# Load test cases from Excel once
CASES = load_login_cases("testdata.xlsx", sheet_name="LoginData")


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.case_id)
def test_login_ddt(driver, case, logger):
    wait = WebDriverWait(driver, 10)

    # Step 1: open login page
    driver.get(LOGIN_URL)

    # Step 2: input credentials
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(case.username)
    driver.find_element(By.ID, "password").send_keys(case.password)

    # Step 3: submit
    driver.find_element(By.ID, "submit").click()

    # Checkpoint: actual outcome equals expected
    actual = get_actual_outcome(driver, wait)
    if actual == case.expected:
        logger.info(f"DATASET {case.case_id} RESULT: PASSED | expected={case.expected} actual={actual}")
    else:
        logger.error(
            f"DATASET {case.case_id} RESULT: FAILED | expected={case.expected} actual={actual} "
            f"| username={case.username} password={case.password}"
    )
    assert actual == case.expected, (
        f"EXPECTED: {case.expected}\n"
        f"ACTUAL: {actual}\n"
        f"DATASET: case_id={case.case_id}, username={case.username}, password={case.password}"
    )
