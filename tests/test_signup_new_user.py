import json
import sys
import os
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# GLOBAL CONSTANTS
with open('data/testData.json', 'r') as file:
    data = json.load(file)

CONTACT_LIST = data["URLS"]["CONTACT_LIST"]
CONTACT_DETAILS = data["URLS"]["CONTACT_DETAILS"]
HOME_PAGE = data["URLS"]["HOME_PAGE"]

from page_objects.base_page import BasePage

def test_sign_up_new_user(driver, new_user):
    page = BasePage(driver)
    page.signup(new_user["first_name"], new_user["last_name"], new_user["email"], new_user["password"])

    assert page.current_url == CONTACT_LIST, \
        "User hasn't been successfully redirected to the Contact List page."

def test_login_existing_user(driver, new_user):
    page = BasePage(driver)
    page.login(new_user)

    assert page.add_a_new_contact_button_is_visible, \
"Log in Failed- couldn't find the 'Add a New Contact' button"


def test_add_new_contact(driver, new_user):
    page = BasePage(driver)
    page.login(new_user)
    page.add_new_contact("Sam2", "Doe2", "SamDoe2@what.com")

    assert page.current_url == CONTACT_LIST, "Not in Contact List page."


def test_edit_existing_contact(driver, new_user):
    page = BasePage(driver)
    page.login(new_user)
    page.click_on_first_contact_in_table(driver)
    page.click_edit()
    page.edit_contact("Adam", "Sandler", "AdamSandlerOG@HotMail.com")
    page.click_submit()
    page.wait_for_redirection(CONTACT_DETAILS)

    assert page.current_url == CONTACT_DETAILS, "redirection falied"


def test_delete_existing_contact(driver, new_user):
    page = BasePage(driver)
    page.login(new_user)
    page.click_on_first_contact_in_table(driver)
    page.click_delete()
    alert = driver.switch_to.alert
    alert.accept()
    page.wait_for_redirection(CONTACT_LIST)
    
    assert page.current_url == CONTACT_LIST, "redirection falied"



def test_logout(driver, new_user):
    page = BasePage(driver)
    page.login(new_user)
    page.click_logout()
    page.wait_for_redirection(HOME_PAGE)

    assert page.current_url == HOME_PAGE, "redirection falied"

# 1. Send POST request with contact data.
# def test_add_new_contact():
#     url = 'https://thinking-tester-contact-list.herokuapp.com/contacts'
#     new_contact = {
#         "firstName": "John",
#         "lastName": "Doe",
#         "birthdate": "1970-01-01",
#         "email": "jdoe@fake.com",
#         "phone": "8005555555",
#         "street1": "1 Main St.",
#         "street2": "Apartment A",
#         "city": "Anytown",
#         "stateProvince": "KS",
#         "postalCode": "12345",
#         "country": "USA"
#     }
#     # Your Bearer token
#     token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzY4NGIzYzA0YjVmMzAwMTNhYzM4ODkiLCJpYXQiOjE3MzQ4ODgyNTJ9.L_T9nj9IfKDV8RIE6hAz5EFf9ddfnd5XU1SvoshmvZo"

#     # Headers including the Authorization
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, json=new_contact, headers=headers)

#     # Check the response
#     # Response status should be 201.
#     if response.status_code == 201:
#         print("Request was successful:", response.json())
#     else:
#         print(f"Failed with status code {response.status_code}: {response.text}")

#     # Response body should contain firstName, lastName, and _id properties.
#     assert response.json().get("firstName"), "First name field is empty"
#     assert response.json().get("lastName"), "Last name field is empty"
#     assert response.json().get("_id"), "_id  field is empty"


# def test_missing_required_field():
#     # 1. Send POST request with incomplete contact data (missing firstName).

#     url = 'https://thinking-tester-contact-list.herokuapp.com/contacts'
#     new_contact = {
#         "firstName": "",
#         "lastName": "Doe",
#         "birthdate": "1970-01-01",
#         "email": "jdoe@fake.com",
#         "phone": "8005555555",
#         "street1": "1 Main St.",
#         "street2": "Apartment A",
#         "city": "Anytown",
#         "stateProvince": "KS",
#         "postalCode": "12345",
#         "country": "USA"
#     }
#     # Your Bearer token
#     token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzY4NGIzYzA0YjVmMzAwMTNhYzM4ODkiLCJpYXQiOjE3MzQ4ODgyNTJ9.L_T9nj9IfKDV8RIE6hAz5EFf9ddfnd5XU1SvoshmvZo"

#     # Headers including the Authorization
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, json=new_contact, headers=headers)

#     # Check the response
#     # 2. Check response status and body.
#     data = response.json()
#     if response.status_code == 400:
#         print("Request was successful:", data)
#     else:
#         print(f"Failed with status code {response.status_code}: {response.text}")

#     # Response body should contain an error message indicating firstName is required.
#     assert 'errors' in data
#     assert data['errors']['firstName']['message'] == 'Path `firstName` is required.'



