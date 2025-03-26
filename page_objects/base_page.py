import json

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from page_objects.contact_list_helper import ContactListHelper

with open('data/testData.json', 'r') as file:
    data = json.load(file)

CONTACT_LIST = data["URLS"]["CONTACT_LIST"]
CONTACT_DETAILS = data["URLS"]["CONTACT_DETAILS"]
HOME_PAGE = data["URLS"]["HOME_PAGE"]
ADD_USER = data["URLS"]["ADD_USER"]
ADD_CONTACT = data["URLS"]["ADD_CONTACT"]

class BasePage(ContactListHelper):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._driver = driver
        self.wait = WebDriverWait(self._driver, 10)

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    def signup(self, first_name: str, last_name: str, email: str, password: str):
        super().open_website()
        super().click_signup()
        super().fill_up_signup_form(first_name, last_name, email, password)
        super().click_submit()
        self.wait.until(ec.url_changes(ADD_USER))

    def login(self, new_user):
        email = new_user["email"]
        password = new_user["password"]
        super().open_website()
        super().fill_up_email_and_password(email, password)
        super().click_submit()
        self.wait.until(ec.url_changes(HOME_PAGE))

    def check_you_are_in_contactDetails_page(self):
        self.wait.until(ec.url_contains(CONTACT_DETAILS))
        assert self._driver.current_url == CONTACT_DETAILS, "User was nor redirected successfully after editing"

    def add_new_contact(self, param, param1, param2):
        add_button_locator = (By.ID, "add-contact")
        self.wait.until(ec.visibility_of_element_located(add_button_locator)).click()
        super().fill_up_add_contact_form(param, param1, param2)
        super().click_submit()
        self.wait.until(ec.url_changes(ADD_CONTACT))

    def contact_has_been_added_successfully(self, first_name, last_name, email, time: int = 10):
        table = self.wait.until(ec.visibility_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.TAG_NAME, "tr")
        expected_data = ['', first_name+' '+last_name, '', email.lower(), '', '', '', '',]

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")  # Get all cells of the row
            row_data = [cell.text for cell in cells]  # Extract text from each cell
            if expected_data == row_data:
                return True

        return False

    def click_on_first_contact_in_table(self, time: int = 10):
        table = self.wait.until(ec.visibility_of_element_located((By.TAG_NAME, "table")))
        self.wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="myTable"]/tr[1]/td[2]'))).click()


    def click_edit(self, time: int = 10):
        edit_button = self._driver.find_element(By.ID, "edit-contact")
        self.wait.until(ec.element_to_be_clickable(edit_button))
        edit_button.click()


    def click_logout(self, time: int = 10):
        logout_button_element = self.wait.until(ec.element_to_be_clickable((By.ID, 'logout')))
        logout_button_element.click()


    def click_delete(self, time: int = 10):
        delete_button = self._driver.find_element(By.ID, "delete")
        self.wait.until(ec.element_to_be_clickable(delete_button))
        delete_button.click()

    def edit_contact(self, first_name, last_name, email):
        super().fill_up_add_contact_form(first_name, last_name, email)

    def wait_for_redirection(self, url: str):
        self.wait.until(ec.url_to_be(url))


