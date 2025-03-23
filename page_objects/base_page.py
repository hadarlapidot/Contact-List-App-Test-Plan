from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from page_objects.contact_list_helper import ContactListHelper


class BasePage(ContactListHelper):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._driver = driver
        self.wait = WebDriverWait(self._driver, 10)

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    def signup(self, first_name: str, last_name: str, email: str, password: str):
        # 1. Navigate to the app's homepage.
        super().open_website()
        # 2. Click ""Sign up"".
        super().click_signup()
        # 3. Fill in the signup form.
        super().fill_up_signup_form(first_name, last_name, email, password)
        # 4. Click ""Submit""."
        super().click_submit()
        self.wait.until(ec.url_changes('https://thinking-tester-contact-list.herokuapp.com/addUser'))

    def login(self, email: str, password: str):
        # 1. Navigate to the homepage
        super().open_website()
        # 2. Fill in login credentials
        super().fill_up_email_and_password(email, password)
        # 3. Click "Submit"
        super().click_submit()
        # wait until redirection
        self.wait.until(ec.url_changes('https://thinking-tester-contact-list.herokuapp.com/'))

    def check_you_are_in_contactDetails_page(self):
        self.wait.until(ec.url_contains('https://thinking-tester-contact-list.herokuapp.com/contactDetails'))
        assert self._driver.current_url == 'https://thinking-tester-contact-list.herokuapp.com/contactDetails', "User was nor redirected successfully after editing"

    def add_new_contact(self, param, param1, param2):
        # 1. Click "Add a New Contact".
        add_button_locator = (By.ID, "add-contact")
        wait = WebDriverWait(self._driver, 10)
        wait.until(ec.visibility_of_all_elements_located(add_button_locator))
        super().click(add_button_locator)
        # 2. Fill in the contact form.
        super().fill_up_add_contact_form(param, param1, param2)
        # 3. Click "Submit".
        super().click_submit()

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
        sleep(4)




