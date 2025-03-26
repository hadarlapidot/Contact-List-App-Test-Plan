# Contact List Automation Testing

## Project Overview

This project contains automated UI and API tests for a Contact List web application. The tests ensure that key user flows, such as signup, login, adding/editing/deleting contacts, and API interactions, work as expected.

## Table of Contents

- [Project Structure](#project-structure)
- [Test Design](#test-design)
  - [End-to-End Tests](#end-to-end-tests)
  - [API Tests](#api-tests)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Running Tests](#running-tests)

## Project Structure

```
contact-list-tests
│-- data
│-- page_objects
│   │-- base_page
│   │-- contact_list_helper
│-- tests
|   |-- test_api.py
|   |-- test_ui.py
│-- conftest.py
│-- README.md
│-- requirements.txt
│-- Test Cases.xlsx
```

## Test Design

### End-to-End Tests

These tests validate the UI functionality of the Contact List application using Selenium.

| Step | Test Name                 | Test Steps                                                                                                           | Expected Results                                                                                     |
| ---- | ------------------------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1    | **Signup New User**       | 1. Navigate to the app's homepage. <br> 2. Click "Sign up". <br> 3. Fill in the signup form. <br> 4. Click "Submit". | User is successfully signed up and redirected to the contact list page.                              |
| 2    | **Login Existing User**   | 1. Navigate to the homepage. <br> 2. Fill in login credentials. <br> 3. Click "Submit".                              | User is logged in successfully and "Add a New Contact" button is visible.                            |
| 3    | **Add New Contact**       | 1. Click "Add a New Contact". <br> 2. Fill in the contact form. <br> 3. Click "Submit".                              | Contact is added successfully. Contact details should be visible.                                    |
| 4    | **Edit Existing Contact** | 1. Select the contact. <br> 2. Click "Edit Contact". <br> 3. Edit details (Address 2). <br> 4. Click "Submit".       | Contact details are updated successfully. Changes are visible on the contact list and details pages. |
| 5    | **Delete Contact**        | 1. Select the contact. <br> 2. Click "Delete Contact". <br> 3. Confirm deletion.                                     | Contact is deleted successfully and should no longer be visible in the contact list.                 |
| 6    | **Logout User**           | 1. Click "Logout".                                                                                                   | User is logged out successfully. The "Sign up" and "Submit" buttons for login are visible.           |

### API Tests

These tests validate the API endpoints using automated requests.

| Step | Test Name                   | Test Steps                                                                                                           | Expected Results                                                                                                        |
| ---- | --------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1    | **Add New Contact**         | 1. Send a `POST` request with contact data. <br> 2. Check response status and body.                                  | Response status should be `201`. <br> Response body should contain `firstName`, `lastName`, and `_id` properties.       |
| 2    | **Missing Required Fields** | 1. Send a `POST` request with incomplete contact data (missing `firstName`). <br> 2. Check response status and body. | Response status should be `400`. <br> Response body should contain an error message indicating `firstName` is required. |

## Technologies Used

- **Selenium** for UI automation
- **Python** for scripting
- **Requests** library for API testing
- **Pytest** for test execution
- **WebDriverWait** for handling dynamic elements

## Setup Instructions

### Prerequisites

- Python 3.x installed
- ChromeDriver or other browser WebDriver installed
- Virtual environment (optional but recommended)

### Installation Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/hadarlapidot/Contact-List-App-Test-Plan.git
   cd Contact-List-App-Test-Plan
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure test data in `data/testData.json`.

## Running Tests

### Running The Tests

```sh
pytest --html=report.html --self-contained-html
```
