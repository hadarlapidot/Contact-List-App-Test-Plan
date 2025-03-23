import os
import time

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from faker import Faker

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    my_driver = webdriver.Chrome(options=options)
    yield my_driver
    my_driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield  # Let pytest do its thing first
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            driver.save_screenshot(filepath)
            print(f"📸 Screenshot saved at: {filepath}")

@pytest.fixture(scope="session")
def new_user():
    """Creates a random user credentials to be used in sign up flow and in login flow, in this order"""
    faker = Faker()

    first = faker.first_name()
    last = faker.last_name()
    email = faker.email()
    password = faker.password(length=10)

    return {
        "first": first,
        "last": last,
        "email": email,
        "password": password
    }