# ERP Login Module

A python package/module to automate login process in ERP for IIT-KGP.

<details>
  <summary>Table of Contents</summary>
   
- <a href="#description">Description</a>
   - <a href="#endpoints">Endpoints</a>
      - <a href="#endpoints-about">About</a>
      - <a href="#endpoints-usage">Usage</a>
      - <a href="#usage-in-login-workflow">Usage in login workflow</a>
   - <a href="#login">Login</a>
      - <a href="#login-input">Input</a>
      - <a href="#login-output">Output</a>
      - <a href="#login-usage">Usage</a>
   - <a href="#session-alive">Session status check</a>
      - <a href="#session-alive-input">Input</a>
      - <a href="#session-alive-output">Output</a>
      - <a href="#session-alive-usage">Usage</a>
- <a href="#package-usage">Usage</a>
   - <a href="#prerequisites">Prerequisites</a>
      - <a href="#erpcreds">ERP credentials file</a>
         - <a href="#erpcreds-creating">Creating</a>
         - <a href="#erpcreds-using">Using</a>
      - <a href="#token">Generating token for GMail enabled googleapi</a>
   - <a href="#example">Example</a>
   
</details>

<div id="description"></div>

## Description

```graphql
iitkgp_erp_login
   ├── endpoints.py
   ├── erp.py
   └── read_mail.py
```

[read_mail.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/read_mail.py) contains the implementation of the `getOTP(OTP_WAIT_INTERVAL)` function, along with various helper functions. These functions are not intended to be used by _you_, the user. The only case where OTP is required is during the login process, which is handled by functions in [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py). Hence, let this script serve as an abstraction for general users. If you want to modify the OTP fetching process, feel free to refer to the [read_mail.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/read_mail.py) script.

<div id="endpoints"></div>

### Endpoints

The [endpoints.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/endpoints.py) file includes all the necessary endpoints for the ERP login workflow.

<div id="endpoints-about"></div>

#### About
- `HOMEPAGE_URL`: The URL of the ERP homepage/loginpage.
- `SECRET_QUESTION_URL`: The URL for retrieving the secret question for authentication.
- `OTP_URL`: The URL for requesting the OTP (One-Time Password) for authentication.
- `LOGIN_URL`: The URL for ERP login.
- `WELCOMEPAGE_URL`: The URL of the welcome page, which is accessible only when the user is **NOT** logged in, and behaves exactly like the `HOMEPAGE_URL`. However, when the user is logged in, it returns a `404` error.

<div id="endpoints-usage"></div>

#### Usage
```python
from iitkgp_erp_login.endpoints import *

print(HOMEPAGE_URL)
# Output: https://erp.iitkgp.ac.in/IIT_ERP3/

print(LOGIN_URL)
# Output: https://erp.iitkgp.ac.in/SSOAdministration/auth.htm
```

<div id="usage-in-login-workflow"></div>

#### Usage in login workflow

To automate the login process into ERP, the endpoints are hit in the following order:

1. Hit `HOMEPAGE_URL` using `session.get(HOMEPAGE_URL)`. This step establishes the initial session and retrieves `sessionToken`.
2. Hit `SECRET_QUESTION_URL` using `session.post(SECRET_QUESTION_URL, data={'user_id': erp_creds.ROLL_NUMBER}, headers=headers)`. This step fetches the secret question required for authentication.
3. Hit `OTP_URL` using `session.post(OTP_URL, data={'typeee': 'SI', 'loginid': erp_creds.ROLL_NUMBER}, headers=headers)`. This step requests an OTP (One-Time Password) for authentication.
4. Finally, hit `LOGIN_URL` using `session.post(LOGIN_URL, data=login_details, headers=headers)`. This step performs the actual ERP login with the provided login details and OTP.

> **Note**  `session` = [requests.Session()](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) is used to persist the session parameters throughout the workflow

<div id="login"></div>

### Login

ERP login workflow is implemented in `login(headers, erp_creds, OTP_WAIT_INTERVAL, session)` function in [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py). The input and output specifications for the function are mentioned below.

<div id="login-input"></div>

#### Input
The function requires following arguments:
1. `headers`: Headers for the post requests. An example is given below.
    ```python
    headers = {
       'timeout': '20',
       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
    }
    ``` 
2.  `erp_creds`: <a href="#erpcreds">ERP Login Credentials file</a>, which is imported into python file.
    ```python
    import erpcreds
    ```
3.  `OTP_WAIT_INTERVAL`: The interval after which the API continuously checks for new OTP mail.
4.  `session`: A [requests.Session()](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) object, to persist the session parameters throughout the workflow.
    ```python
    import requests

    session = requests.Session()
    ```

<div id="login-output"></div>

#### Output
1. The function returns the following in the order of occurrence as here (`sessionToken, ssoToekn`):
   1. [sessionToken](https://en.wikipedia.org/wiki/Session_ID)
   2. [ssoToken](https://en.wikipedia.org/wiki/Single_sign-on)
2. It also modifies the `session` object, which now includes parameters for the logged-in session. These parameters can be utilized for further navigation within the ERP system.
3. It incorporates **comprehensive logging**. It prints the status of each step, providing detailed information throughout the process.

<div id="login-usage"></div>

#### Usage
It is recommended to use the `login` function in the following manner:
```python
# importing the erp.py file
import iitkgp_erp_login.erp as erp

# using the login function inside erp.py
sessionToken, ssoToken = erp.login(headers, erpcreds, 2, session)
```

Here's an example combining all the aspects we have discussed so far about the `login` function:

```python
import requests
import erpcreds
import iitkgp_erp_login.erp as erp

headers = {
   'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

session = requests.Session()

sessionToken, ssoToken = erp.login(headers, erpcreds, 2, session)
   
print(sessionToken, ssoToken)
```

> **Note** The code snippet above will not work unless the <a href="#prerequisites">prerequisites</a> are fulfilled

<div id="session-alive"></div>

### Session status check
The logic for checking the status of the session is implemented in the `session_alive(session)` function  n [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py). This function determines whether the given session is valid/alive or not. The input and output specifications for the function are mentioned below.

<div id="session-alive-input"></div>

#### Input
The function requires following argument:

 -  `session`: [requests.Session()](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) object, to persist the session parameters throughout the workflow.
    ```python
    import requests

    session = requests.Session()
     ```
<div id="session-alive-output"></div>

#### Output
The `session_alive(session)` function returns the status of the session as a boolean value: **True** if it is alive and **False** if it is not.

<div id="session-alive-usage"></div>

#### Usage
It is recommended to use the `session_alive` function in the following manner:
```python
# Importing the erp.py file
import iitkgp_erp_login.erp as erp

# Using the session_alive function inside erp.py
print(erp.session_alive(session))
```

Here's an example combining all the aspects we have discussed so far about the `login` function and `session_alive` function:

```python
import requests
import time
import creds
import iitkgp_erp_login.erp as erp

headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

session = requests.Session()

while True:
    if not erp.session_alive(session):
        erp.login(headers, creds, 2, session)
    else:
        print("Session is alive.")

    time.sleep(2)
```

> **Note** The code snippet above will not work unless the <a href="#prerequisites">prerequisites</a> are fulfilled

<div id="package-usage"></div>

## Usage

<div id="prerequisites"></div>

### Prerequisites

The following scripts are required and **MUST** be present in the same directory as the script where `iitkgp_erp_login` module is being imported:

- <a href="#erpcreds">erpcreds.py</a>
- <a href="#token">token.json</a>

<div id="erpcreds"></div>

#### ERP credentials file

<div id="erpcreds-creating"></div>

##### Creating

Create a `.py` file with your ERP credentials stored in it. Please follow the instructions below to create this file:
- You can choose any valid name for the file, adhering to Python's naming conventions.
- **Do not change the variable names**. Simply copy the format provided below and update the values inside the `double quotes` (").
  ```python
  # ERP Credentials
  ROLL_NUMBER = "XXYYXXXXX"
  PASSWORD = "**********"
  SECURITY_QUESTIONS_ANSWERS = {
      "Q1" : "A1",
      "Q2" : "A2",
      "Q3" : "A3",
  }
  ```

<div id="erpcreds-using"></div>

##### Using

Let's suppose you have saved the ERP credentials file as `erpcreds.py`. To use it, you can simply import it in your Python script using the following code:

```python
import erpcreds

print(erpcreds.ROLL_NUMBER)
# Output: XXYYXXXXX

print(erpcreds.SECURITY_QUESTIONS_ANSWERS["Q2"])
# Output: A2
```

<div id="token"></div>

#### Generating token for GMail enabled googleapi

1. Follow the steps in the [Gmail API - Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) guide to obtain `credentials.json` file.
   > **Note** The `credentials.json` file is permanent unless you manually delete its reference in your Google Cloud Console.

2. To generate the `token.json` file, follow the steps below:
    - Download the [gentokenjson.py](https://gist.github.com/proffapt/adbc716a427c036f238e828d8995e1a3) file and place it in the same folder that contains the `credentials.json` file
    - Import the required module, `google-auth-oauthlib`
      
      ```bash
      pip install google-auth-oauthlib
      ```
    - Execute `gentokenjson.py` with the `readonly` argument
   
      ```bash
      python3 gentokenjson.py readonly
      ```
    - A browser window will open, prompting you to select the Google account associated with receiving OTP for login.
    - Grant permission to the selected email address to utilize the newly enabled **Gmail API**.
       - Click on `Continue` instead of __Back To Safety__
       - Then, press `Continue` again
    - The `token.json` file will be generated in the same folder as the `credentials.json` file
  
    > **Warning** The `token.json` file has an expiration time, so it's important to periodically check and refresh it in your projects to ensure uninterrupted access.

<div id="example"></div>

### Example

Now, we will create a script that opens the ERP system on your default browser with a logged-in session.

1. Install the package.

   ```bash
   pip install iitkgp_erp_login
   ````
2. Make sure that <a href="#erpcreds">erpcreds.py</a> & <a href="#token">token.json</a> files exist in the same directory as the script we are about to create.

3. Create a file named `open_erp.py` and include the following code:

   ```python
   import requests
   import webbrowser
   import erpcreds
   import iitkgp_erp_login.erp as erp
   from iitkgp_erp_login.endpoints import HOMEPAGE_URL

   headers = {
       'timeout': '20',
       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
   }

   session = requests.Session()

   _, ssoToken = erp.login(headers, erpcreds, 2, session)

   logged_in_url = f"{HOMEPAGE_URL}?ssoToken={ssoToken}"
   webbrowser.open(logged_in_url)
   ```
4. Run the script.
   ```bash
   python3 open_erp.py
   ```
