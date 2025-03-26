import random
import string

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



class ContactListHelper:
    def __init__(self, driver: WebDriver):
        self._driver = driver
        self.wait = WebDriverWait(self._driver, 10)
        # LOCATORS
        # main page
        self._signup_button = (By.ID, "signup")
        self._submit_button = (By.ID, "submit")
        # sign up page
        self._signup_firstname_textfield = (By.ID, "firstName")
        self._signup_lastname_textfield = (By.ID, "lastName")
        self._signup_email_textfield = (By.ID, "email")
        self._signup_password_textfield = (By.ID, "password")
        # contact list page
        self._add_a_new_contact_button = (By.ID, "add-contact")
        # Add Contact

    def find_by_id(self, locator) -> WebElement:
        return self._driver.find_element(*locator)

    def open_website(self):
        self._driver.get("https://thinking-tester-contact-list.herokuapp.com/")

    def click_signup(self):
        sign_up_btn = self.wait_until_clickable(self._signup_button)
        sign_up_btn.click()

    def click_submit(self):
        submit_btn = self.wait_until_clickable(self._submit_button)
        submit_btn.click()

    def click(self, locator):
        btn = self.wait_until_clickable(locator)
        btn.click()

    def wait_until_element_is_visible(self, locator: tuple, time: int = 10):
        self.wait.until(ec.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator: tuple, time: int = 10):
        return self.wait.until(ec.element_to_be_clickable(locator))

    # def get_header(self, time: int = 10):
    #     header = self.wait.until(
    #         ec.visibility_of_element_located((By.TAG_NAME, "h1")))
    def fill_up_signup_form(self, first_name, last_name, email, password):
        self.fill_up_name(first_name, last_name)
        self.fill_up_email_and_password(email, password)

    def fill_up_email_and_password(self, email, password):
        self.wait_until_element_is_visible(self._signup_email_textfield)
        self.find_by_id(self._signup_email_textfield).send_keys(email)
        self.find_by_id(self._signup_password_textfield).send_keys(password)

    def fill_up_name(self, first_name: str, last_name: str):
        # first name
        text_field = self.find_by_id(self._signup_firstname_textfield)
        self.clear_input_field(text_field)
        text_field.send_keys(first_name)
        # last name
        text_field = self.find_by_id(self._signup_lastname_textfield)
        self.clear_input_field(text_field)
        text_field.send_keys(last_name)

    @property
    def add_a_new_contact_button_is_visible(self):
        return ec.visibility_of_element_located(self._add_a_new_contact_button)

    def fill_up_add_contact_form(self, first_name: str, last_name: str, email: str):
        self.fill_up_name(first_name, last_name)
        text_field = self.find_by_id(self._signup_email_textfield)
        self.clear_input_field(text_field)
        text_field.send_keys(email)

    # seems like clear() doesnt always work...
    def clear_input_field(self, input_field):
        i=30
        while i>0:
            input_field.send_keys(Keys.BACKSPACE)
            i = i-1

    def generate_random_mail_address(self):
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return f"{username}@example.com"
