from selenium import webdriver
import pytest


@pytest.fixture(scope="module")
def driversetup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()