# GuestBook

## Overview

This project is a simple API that allows users to create entries, retrieve paginated entries, and fetch data for each user including their last entry details.

## Installation

1. Clone the repository:

    ```
    git clone git@github.com:canerkaraguler/GuestBook.git
    ```

2. Navigate to the project directory:

    ```
    cd project_directory
    ```

3. Create and activate a virtual environment:

    - Using Anaconda:

        ```
        conda create --name venv
        conda activate venv
        ```

    - Using standard Python:

        ```
        python -m venv venv
        source venv/bin/activate
        ```

4. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the Django development server:

    ```
    python manage.py runserver
    ```

2. Run tests:

    ```
    python manage.py test
    ```
3. Access the API endpoints using the base URL:

    ```
    http://localhost:8000/api/
    ```

## Endpoints

### Create Entry

- **URL**: `/create-entry/`
- **Method**: POST
- **Description**: Creates a new entry based on the submitted form data.
- **Example Request**:
    ```
    POST /api/create-entry/
    {
        "name": "Caner Karagüler",
        "subject": "Demo",
        "message": "Demo Message"
    }
    ```


### Get Entries

- **URL**: `/get-entries/`
- **Method**: GET
- **Description**: Retrieves paginated and sorted entries from the database.

### Get Users Data

- **URL**: `/get-users-data/`
- **Method**: GET
- **Description**: Retrieves data for each user, including the total count of messages and details of their last entry.

## Notes

- Function-based views are preferred over class-based views for simplicity.
- In Get Users Data end point, there is  no total count of messages in the example response but it was added to the response as this requirement is declared on the project description
