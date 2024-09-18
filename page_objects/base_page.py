from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from page_objects.classmethod import ClassMethods


class BasePage(ClassMethods):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._driver = driver

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    def signup(self, first_name: str, last_name: str, email: str, password: str):
        # 1. Navigate to the app's homepage.
        super()._open_website()
        # 2. Click ""Sign up"".
        super()._click_signup()
        # 3. Fill in the signup form.
        super().fill_up_signup_form(first_name, last_name, email, password)
        # 4. Click ""Submit""."
        super().click_submit()
        sleep(5)

    def login(self, email: str, password: str):
        # 1. Navigate to the homepage
        super()._open_website()
        # 2. Fill in login credentials
        super().fill_up_email_and_password(email, password)
        # 3. Click "Submit"
        super().click_submit()

    def check_you_are_in_contactlist_page(self):
        current_url = self.current_url
        return current_url == "https://thinking-tester-contact-list.herokuapp.com/contactDetails"

    def add_new_contact(self, param, param1, param2):
        # 1. Click "Add a New Contact".
        add_button_locator = (By.ID, "add-contact")
        super()._wait_until_element_is_clickable(add_button_locator)
        super().click(add_button_locator)
        # 2. Fill in the contact form.
        super().fill_up_add_contact_form(param, param1, param2)
        # 3. Click "Submit".
        super().click_submit()

    def contact_has_been_added_successfully(self, first_name, last_name, email, time: int = 10):
        wait = WebDriverWait(self._driver, time)
        table = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.TAG_NAME, "tr")
        expected_data = ['', first_name+' '+last_name, '', email.lower(), '', '', '', '',]

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")  # Get all cells of the row
            row_data = [cell.text for cell in cells]  # Extract text from each cell
            if expected_data == row_data:
                return True

        return False

    # def click_on_first_contact_in_table(self, time: int = 10):
    #     # find <tr> in DOM
    #     wait = WebDriverWait(self._driver, 10)
    #     table = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "table")))
    #     row = table.find_element(By.CLASS_NAME, "contactTableBodyRow")
    #     wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "contactTableBodyRow")))
    #     # click on it
    #     row.click()

    def click_on_first_contact_in_table(self, time: int = 10):
        wait = WebDriverWait(self._driver, 10)
        table = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "table")))
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="myTable"]/tr[1]/td[2]'))).click()


    def click_edit(self, time: int = 10):
        wait = WebDriverWait(self._driver, time)
        edit_button = self._driver.find_element(By.ID, "edit-contact")
        wait.until(ec.element_to_be_clickable(edit_button))
        edit_button.click()

    def click_logout(self, time: int = 10):
        wait = WebDriverWait(self._driver, time)
        logout_button = self._driver.find_element(By.ID, "logout")
        wait.until(ec.element_to_be_clickable(logout_button))
        logout_button.click()


    def click_delete(self, time: int = 10):
        wait = WebDriverWait(self._driver, time)
        delete_button = self._driver.find_element(By.ID, "delete")
        wait.until(ec.element_to_be_clickable(delete_button))
        delete_button.click()

    def edit_contact(self, first_name, last_name, email):
        super().fill_up_add_contact_form(first_name, last_name, email)
        sleep(4)




