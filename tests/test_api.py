import json
import sys
import os
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# GLOBAL CONSTANTS
with open('data/testData.json', 'r') as file:
    data = json.load(file)

CONTACTS= data["URLS"]["CONTACTS"]
VALID_CONTACT = data["NEW_CONTACTS"]["VALID"]
INVALID_CONTACT = data["NEW_CONTACTS"]["INVALID"]
FIRST_NAME_MISSING_ERROR = data["ERRORS"]["FIRST_NAME_MISSING"]


# MISSING_FIRST_NAME = data["NEW_CONTACTS"]["MISSING_FIRST_NAME"]
TOKEN = data["TOKEN"]


# 1. Send POST request with contact data.
def test_add_new_contact():
    url = CONTACTS
    new_contact = VALID_CONTACT

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=new_contact, headers=headers)
    json = response.json()

    # Check the response
    # Response status should be 201.
    if response.status_code == 201:
        print("Request was successful:", response.json())
        # Response body should contain firstName, lastName, and _id properties.
        assert json.get("firstName"), "First name field is empty"
        assert json.get("lastName"), "Last name field is empty"
        assert json.get("_id"), "_id  field is empty"
    else:
        assert response.status_code == 201
        print (f"Failed with status code {response.status_code}: {response.text}")




def test_missing_required_field():
    # 1. Send POST request with incomplete contact data (missing firstName).

    url = CONTACTS
    new_contact = INVALID_CONTACT
    token = TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=new_contact, headers=headers)
    data = response.json()

    if response.status_code == 400:
        assert 'errors' in data
        error = data['errors']['firstName']['message']
        assert error == FIRST_NAME_MISSING_ERROR
    else:
        assert response.status_code == 400
        print(f"Failed with status code {response.status_code}: {response.text}")

    
