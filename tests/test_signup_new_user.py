from time import sleep
import requests
import pytest
from page_objects.base_page import BasePage


def test_sign_up_new_user(driver):
    page = BasePage(driver)
    page.signup("Sam", "Doe", "SamDoe@what.com", "cupcakes")
    # User is successfully signed up and redirected to the contact list page.
    assert page.current_url == "https://thinking-tester-contact-list.herokuapp.com/contactList", \
        "Not in Contact List page."


def test_login_existing_user(driver):
    page = BasePage(driver)
    page.login("SamDoe@what.com", "cupcakes")
    # User is logged in successfully and "Add a New Contact" button is visible.
    assert page.add_a_new_contact_button_is_visible(), \
        "Log in Failed- couldn't find the 'Add a New Contact' button"


def test_add_new_contact(driver):
    page = BasePage(driver)
    test_login_existing_user(driver)
    page.add_new_contact("Sam2", "Doe2", "SamDoe2@what.com")
    # Contact is added successfully. Contact details should be visible.
    assert page.current_url == "https://thinking-tester-contact-list.herokuapp.com/contactList", \
        "Not in Contact List page."
    assert page.contact_has_been_added_successfully("Sam2", "Doe2", "SamDoe2@what.com", 2)


def test_edit_existing_contact(driver):
    page = BasePage(driver)
    test_login_existing_user(driver)
    # 1. Select the contact
    page.click_on_first_contact_in_table(driver)
    # 2. Click "Edit Contact".
    page.click_edit()
    # 3. Edit details (Address 2).
    page.edit_contact("Adam", "Sandler", "AdamSandlerOG@HotMail.com")
    # 4. Click "Submit".
    page.click_submit()

    assert page.check_you_are_in_contactlist_page(), "It didn't work..."


def test_delete_existing_contact(driver):
    # 1. Select the contact
    page = BasePage(driver)
    test_login_existing_user(driver)
    # 1. Select the contact
    page.click_on_first_contact_in_table(driver)
    # 2. Click "Delete Contact".
    page.click_delete()
    alert = driver.switch_to.alert
    alert.accept()
    sleep(2)
    # 3. Confirm deletion.
    # --missing--


def test_logout(driver):
    page = BasePage(driver)
    test_login_existing_user(driver)
    # 1. Click "Logout".
    page.click_logout()


# 1. Send POST request with contact data.
def test_add_new_contact():
    url = 'https://thinking-tester-contact-list.herokuapp.com/contacts'
    new_contact = {
        "firstName": "John",
        "lastName": "Doe",
        "birthdate": "1970-01-01",
        "email": "jdoe@fake.com",
        "phone": "8005555555",
        "street1": "1 Main St.",
        "street2": "Apartment A",
        "city": "Anytown",
        "stateProvince": "KS",
        "postalCode": "12345",
        "country": "USA"
    }
    # Your Bearer token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NmRkYzJmZmM0MGM5MDAwMTM0M2M0ZDEiLCJpYXQiOjE3MjY1MDM0NzN9.xtb2cl-1gHQHM8v3hzi9ZCqBvrNJYKNW4Rc3VEYfvOA"

    # Headers including the Authorization
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=new_contact, headers=headers)

    # Check the response
    # Response status should be 201.
    if response.status_code == 201:
        print("Request was successful:", response.json())
    else:
        print(f"Failed with status code {response.status_code}: {response.text}")

    # Response body should contain firstName, lastName, and _id properties.
    assert response.json().get("firstName"), "First name field is empty"
    assert response.json().get("lastName"), "Last name field is empty"
    assert response.json().get("_id"), "_id  field is empty"


@pytest.mark.debug
def test_missing_required_field():
    # 1. Send POST request with incomplete contact data (missing firstName).

    url = 'https://thinking-tester-contact-list.herokuapp.com/contacts'
    new_contact = {
        "firstName": "",
        "lastName": "Doe",
        "birthdate": "1970-01-01",
        "email": "jdoe@fake.com",
        "phone": "8005555555",
        "street1": "1 Main St.",
        "street2": "Apartment A",
        "city": "Anytown",
        "stateProvince": "KS",
        "postalCode": "12345",
        "country": "USA"
    }
    # Your Bearer token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NmRkYzJmZmM0MGM5MDAwMTM0M2M0ZDEiLCJpYXQiOjE3MjY1MDM0NzN9.xtb2cl-1gHQHM8v3hzi9ZCqBvrNJYKNW4Rc3VEYfvOA"

    # Headers including the Authorization
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=new_contact, headers=headers)

    # Check the response
    # 2. Check response status and body.
    data = response.json()
    if response.status_code == 400:
        print("Request was successful:", data)
    else:
        print(f"Failed with status code {response.status_code}: {response.text}")

    # Response body should contain an error message indicating firstName is required.
    assert 'errors' in data
    assert data['errors']['firstName']['message'] == 'Path `firstName` is required.'



