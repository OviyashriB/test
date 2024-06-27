from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import datetime ,os, pytest


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

    def find_element(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            return element
        except NoSuchElementException:
            return None

    def wait_for_element_to_be_clickable(self, by, value):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, value)))
            return element
        except TimeoutException:
            return None

    def wait_for_element_to_be_visible(self, by, value):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((by, value)))
            return element
        except TimeoutException:
            return None

    def capture_screenshot_on_failure(driver, test_name):
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_filename = f"{test_name}_{current_time}.png"
            screenshot_path = os.path.join("screenshots", screenshot_filename)
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved as {screenshot_path}")
        except Exception as e:
            print(f"Failed to capture screenshot: {str(e)}")
    
    def enter_text(driver, locator, text):
        element_name = locator[0]
        element = driver.wait_for_element_to_be_visible(*locator)
        if element:
            try:
                element.clear()
                element.send_keys(text)
            except StaleElementReferenceException:
                print("Element became stale during text entry. Retrying...")
                element = driver.wait_for_element_to_be_visible(*locator)
                element.clear()
                element.send_keys(text)
            except Exception as e:
                print(f"Failed to enter text in element {element_name}: {e}")
                pytest.fail(f"Failed to enter text in element {element_name}: {e}", pytrace=False)
        else:
            print(f"Element not found: {locator}")
            pytest.fail(f"Element not found: {locator}", pytrace=False)
            
    def click_element(driver, locator):
        element_name = locator[0]
        element = driver.wait_for_element_to_be_clickable(*locator)
        if element:
            try:
                element.click()
            except StaleElementReferenceException:
                print("Element became stale during click. Retrying...")
                element = driver.wait_for_element_to_be_clickable(*locator)
                element.click()
            except Exception as e:
                print(f"Failed to click element {element_name}: {e}")
                pytest.fail(f"Failed to click element {element_name}: {e}", pytrace=False)
        else:
            print(f"Element not found: {locator}")
            pytest.fail(f"Element not found: {locator}", pytrace=False)