import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import logging


qa_logger = logging.getLogger("qa")
qa_logger.setLevel(logging.INFO)

if not qa_logger.handlers:
    file_handler = logging.FileHandler("test_execution.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(formatter)
    qa_logger.addHandler(file_handler)


def pytest_addoption(parser):
    parser.addoption("--mode", action="store", default="local", help="local or cloud")
    parser.addoption("--browser", action="store", default="chrome", help="chrome or firefox")


@pytest.fixture
def logger():
    return qa_logger

@pytest.fixture
def driver(request, logger):
    mode = request.config.getoption("--mode")
    browser = request.config.getoption("--browser")

    logger.info("=== Browser session START ===")

    if mode == "cloud":
        if browser == "firefox":
            options = FirefoxOptions()
        else:
            options = ChromeOptions()

        options.browser_version = "latest"
        options.platform_name = "Windows 11"

        sauce_options = {
            "username": "oauth-galymzhanulyibragim-b1cf8",
            "accessKey": "e4c5541f-2ea1-41f3-94dc-0bee428f0e25",
            "build": "selenium-build-0HL6E",
            "name": request.node.name,
        }

        options.set_capability("sauce:options", sauce_options)

        driver = webdriver.Remote(
            command_executor="https://ondemand.eu-central-1.saucelabs.com:443/wd/hub",
            options=options,
        )
    else:
        driver = webdriver.Chrome()

    yield driver

    driver.quit()
    logger.info("=== Browser session END ===")
