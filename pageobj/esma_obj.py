from .basepage import BasePage
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
from PIL import Image
import io, time, datetime
from datetime import timedelta
import requests
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class Esma_obj(BasePage):
    
    esma_url = "https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_radar"
    accept_cookies = (By.XPATH,"//button[(text(),'Accept')]")
    issuer_name = (By.XPATH,"//input[@name='issuerName']")
    captcha_img = (By.XPATH,"//img[@id='captchaImg']")
    captcha_input = (By.XPATH,"//img[@id='captchaImg']/following::input[1]")
    search_button = (By.XPATH,"//button[contains(text(),'Search')]")
    view_details_element = (By.XPATH,"//td[contains(., 'Fitch')]/following-sibling::td//img[@title='View Details']")
    next_page_button = (By.XPATH,"//li[contains(@class,'next')]")
    last_page_verification = (By.XPATH,"//li[@class='next']/preceding::li[1]")
    last_rating_update = (By.XPATH,"//td[contains(.,'Last rating update')]/following-sibling::td")
    expand_rating_history = (By.XPATH,"//h2/span")
    rating_history_verification = (By.XPATH,"//tbody[@id='definitionsTableBody']//td[1]")
    
    def __init__(self, driver):
        super().__init__(driver)
        

    def open_base_url(self):
        try:
            self.driver.get(self.esma_url)
        except Exception as e:
            print(f"Failed to open URL: {e}")

    def _enter_captcha_manually(self):        
        captcha_input_locator = self.captcha_input 
        captcha_text = input("Please enter the captcha: ")
        time.sleep(3)
        self.enter_text(captcha_input_locator, captcha_text) 
        time.sleep(2)
        search_button_locator = self.search_button  
        self.click_element(search_button_locator)  
        time.sleep(3)
            
    def _count_view_details_elements(self):
        found_details = 0
        last_page_verification = (By.XPATH, "//li[@class='next']/preceding::li[1]")
        last_page_element = None

        while True:
            try:
                view_details_elements = self.driver.find_elements(*self.view_details_element)
                elements = len(view_details_elements)
                found_details += len(view_details_elements)

                if last_page_element == self.find_element(*last_page_verification):
                    break

                last_page_element = self.find_element(*last_page_verification)
                if elements > 0:
                    for i in range(elements):
                        element_individual = f"(//td[contains(., 'Fitch')]/following-sibling::td//img[@title='View Details'])[{i + 1}]"
                        element_xpath = self.find_element(By.XPATH, element_individual)
                        element_xpath.click()
                        time.sleep(2)
                        date_element = self.find_element(*self.last_rating_update) 
                        print(f"Element {i + 1}: {date_element.text}")
                        
                        expand_button = self.find_element(*self.expand_rating_history)
                        expand_button.click()
                        time.sleep(2)
                        
                        rating_verification_element = self.driver.find_elements(*self.rating_history_verification)
                        rating_updated = False
    
                        for verification in rating_verification_element:
                            verification_text = verification.text
                            verification_date = datetime.datetime.strptime(verification_text, "%Y-%m-%d")
                            previous_day = verification_date - timedelta(days=1)
                            
                            if date_element.text == verification_date or previous_day:
                                print("Rating has been updated correctly.")
                                rating_updated = True
                                break
                        
                        if not rating_updated:
                            print("Error: Date doesn't match any in rating history.")

                        self.driver.back()
                        time.sleep(5)

                elif elements < 0:
                    print("No data found.")
                
                self.click_element(self.next_page_button)
                time.sleep(2)
            except NoSuchElementException:
                print("No more pages found. Exiting...")
                break
            
        print(f"Total 'Fitch Ratings Limited ' elements found: {found_details}")




    #element-count
    # def count_view_details_elements(self):
    #     found_details = 0
    #     last_page_verification = (By.XPATH, "//li[@class='next']/preceding::li[1]")
    #     last_page_element = None

    #     while True:
    #         try:
    #             view_details_elements = self.driver.find_elements(*self.view_details_element)
    #             found_details += len(view_details_elements)

    #             if last_page_element == self.find_element(*last_page_verification):
    #                 break
                
    #             last_page_element = self.find_element(*last_page_verification)
                
    #             for idx, element in enumerate(view_details_elements):
    #                 element.click()
    #                 time.sleep(3)
                    
    #                 date_element = self.find_element(*self.last_rating_update) 
    #                 print(f'{idx} : {date_element.text}')

    #                 self.driver.back()
    #                 time.sleep(6)

    #             next_page_button = self.find_element(*self.next_page_button)
    #             self.click_element(self.next_page_button)
    #             time.sleep(1)
    #         except NoSuchElementException:
    #             print("No more pages found. Exiting...")
    #             break
                
    #     print(f"Total 'View Details' elements found: {found_details}")


    #dynamically changing captchas proof
    # def enter_captcha(self, driver):
    #     while True:
    #         # Find the captcha image element
    #         try:
    #             captcha_img = driver.find_element(*self.captcha_img)
    #         except NoSuchElementException:
    #             print("Captcha image not found. Exiting captcha entry.")
    #             break

    #         captcha_img_url = captcha_img.get_attribute("src")

    #         response = requests.get(captcha_img_url)
    #         if response.status_code == 200:
    #             with open("captcha.png", "wb") as file:
    #                 file.write(response.content)

    #             # Use pytesseract to recognize text in the captcha image
    #             captcha_text = self.read_captcha_text("captcha.png")

    #             print("Captcha:", captcha_text)

    #             time.sleep(2)
    #             captcha_input_elem = driver.find_element(*self.captcha_input)
    #             captcha_input_elem.clear()  # Clear the input field
    #             captcha_input_elem.send_keys(captcha_text)

    #             time.sleep(2)
    #             search_button_elem = driver.find_element(*self.search_button)
    #             search_button_elem.click()
    #             time.sleep(3)

    #         else:
    #             print("Failed to fetch captcha image")

    # def read_captcha_text(self, image_path):
    #     try:
    #         captcha_image = Image.open(image_path)
    #         captcha_text = pytesseract.image_to_string(captcha_image)
    #         return captcha_text
    #     except Exception as e:
    #         print(f"Error reading captcha: {str(e)}")
    #         return ""