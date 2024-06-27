from pageobj.esma_obj import Esma_obj
import pytest, time
from pageobj.basepage import BasePage
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException


# @pytest.mark.execution_order(order=1)
def test_esma(driversetup):
    driver = driversetup
    esma = Esma_obj(driver)
    
    esma.open_base_url()
    time.sleep(2)

    try:
        esma.click_element(esma.accept_cookies)
        time.sleep(2)
    except (NoSuchElementException, AssertionError, InvalidSelectorException, Exception)  as e:
        BasePage.capture_screenshot_on_failure(driver,"Accept cookies input not found")
        pytest.fail(f'''Accept cookies Element not found: {e} 
                Check the element still exists or it's Xpath has been changed!''', pytrace=False)
    try:
        esma.enter_text(esma.issuer_name, "xiaomi best time international limited")
        time.sleep(2)
    except (NoSuchElementException, AssertionError, InvalidSelectorException, Exception)  as e:
        BasePage.capture_screenshot_on_failure(driver,"Issuer input not found")
        pytest.fail(f'''Issuer input Element not found: {e} 
                Check the element still exists or it's Xpath has been changed!''', pytrace=False)
        
    esma._enter_captcha_manually()
    
    esma._count_view_details_elements()
    
    driver.close()
    