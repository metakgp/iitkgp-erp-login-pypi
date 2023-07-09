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

[read_mail.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/read_mail.py) contains implementation of `getOTP(OTP_WAIT_INTERVAL)` function along with various helper functions for it. These functions are not intended to be used by _you_ - the user - as the only case, where, OTP will be required is during the login process which is handled by functions in [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py). Hence, let this script be an abstraction for general user. Obviously, if you want to tweak the OTP fetching process feel free to have a look at the script [read_mail.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/read_mail.py).

<div id="endpoints"></div>

### Endpoints

[endpoints.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/endpoints.py) contains all the required endpoints for the ERP login workflow.

<div id="endpoints-about"></div>

#### About
- `HOMEPAGE_URL`: The URL of the ERP homepage/loginpage.
- `SECRET_QUESTION_URL`: The URL for retrieving the secret question for authentication.
- `OTP_URL`: The URL for requesting the OTP (One-Time Password) for authentication.
- `LOGIN_URL`: The URL for ERP login.
- `WELCOMEPAGE_URL`: The URL of the welcome page, which is only accessible when the user is **NOT** logged-in and behaves exactly as `HOMEPAGE_URL` but when logged-in returns `404` error.

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

To automate login into ERP, the endpoints are hit in the following order:

1. Hit `HOMEPAGE_URL` using `session.get(HOMEPAGE_URL)`. This step is necessary to establish the initial session and retrieve `sessionToken`.
2. Hit `SECRET_QUESTION_URL` using `session.post(SECRET_QUESTION_URL, data={'user_id': erp_creds.ROLL_NUMBER}, headers=headers)`. This step fetches the secret question required for authentication.
3. Hit `OTP_URL` using `session.post(OTP_URL, data={'typeee': 'SI', 'loginid': erp_creds.ROLL_NUMBER}, headers=headers)`. This step requests an OTP (One-Time Password) for authentication.
4. Finally, hit `LOGIN_URL` using `session.post(LOGIN_URL, data=login_details, headers=headers)`. This step performs the actual ERP login with the provided login details and OTP.

> **Note**  `session` = [requests.Session()](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) is used to persist the session parameters throughout the workflow

<div id="login"></div>

### Login

ERP Login workflow is implemented in : `login(headers, erp_creds, OTP_WAIT_INTERVAL, session)` inside [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py).<br>
The input and output specifications for the function are mentioned below.

<div id="login-input"></div>

#### Input
The function requires following arguments:
1. `headers`: Headers for the post requests.
    ```python
    headers = {
       'timeout': '20',
       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
    }
    ``` 
2.  `erp_creds`: <a href="#erpcreds">ERP Login Credentials file</a>, which is imported.
    ```python
    import erpcreds
    ```
3.  `OTP_WAIT_INTERVAL`: Interval after which api checks continuously for new OTP mail.
4.  `session`: [requests.Session()](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) object, to persist the session parameters throughout the workflow.
    ```python
    import requests

    session = requests.Session()
    ```

<div id="login-output"></div>

#### Output
1. The function returns:
   - [sessionToken](https://en.wikipedia.org/wiki/Session_ID)
   - [ssoToken](https://en.wikipedia.org/wiki/Single_sign-on)
2. It also modifies the `session` object which now contains parameters for the logged in session, which can be used for further navigation in ERP.
3. Has exhastive loggin inbuilt. It prints the status of each step.

<div id="login-usage"></div>

#### Usage
It is recommended to use the login function as shown below:
```python
# importing the erp.py file
import iitkgp_erp_login.erp as erp

# using the login function inside erp.py
sessionToken, ssoToken = erp.login(headers, erpcreds, 2, session)
```

Combining everything we looked about the `login` function till now:

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

<div id="session-alive"></div>

### Session status check
The logic for status check of session is implemented in `session_alive(session)`. It tells whether the given session is valid/alive or not.<br>
The input and output specifications for the function are mentioned below.

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
Returns the status of session in boolean. __True if alive and False if not__.

<div id="session-alive-usage"></div>

#### Usage
It is recommended to use the session_alive function as shown below:
```python
# importing the erp.py file
import iitkgp_erp_login.erp as erp

# using the session_alive function inside erp.py
print(erp.session_alive(session))
```

Combining everything we looked about the `session_alive` and `login` functions till now:
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

<div id="package-usage"></div>

## Usage

<div id="prerequisites"></div>

### Prerequisites
Following scripts are required, and **MUST** be present in the same directory as that of the script in which `iitkgp_erp_login` (yes, this module) is being imported.

- <a href="#erpcreds">erpcreds.py</a>
- <a href="#token">token.json</a>

<div id="erpcreds"></div>

#### ERP credentials file

<div id="erpcreds-creating"></div>

##### Creating

Create a `.py` file with your ERP credentials stored in it.<br>
Following are the instructions for creating this file:
- Name of the file can be any valid python file's name
- **Variable names must not be changed**, copy the below format and **ONLY update values** inside `"` - _double quotes_.
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

Let's suppose you saved the erp creds file as `erpcreds.py`. Then in order to use it you will just have to import it:
```python
import erpcreds

print(erpcreds.ROLL_NUMBER)
# Output: XXYYXXXXX

print(erpcreds.SECURITY_QUESTIONS_ANSWERS["Q2"])
# Output: A2
```

<div id="token"></div>

#### Generating token for GMail enabled googleapi

1. Follow the steps at [Gmail API - Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) guide to get `credentials.json`.
   > **Note** `credentials.json` is permanent until you delete it in your google clound console.

2. Follow the steps below to generate `token.json`:
    - Download [gentokenjson.py](https://gist.github.com/proffapt/adbc716a427c036f238e828d8995e1a3) in the same folder containing `credentials.json`
    - Import the required module
      
      ```bash
      pip install google-auth-oauthlib
      ```
    - Execute `gentokenjson.py` with `readonly` argument
   
      ```bash
      python3 gentokenjson.py readonly
      ```
    - Browser window will open and ask you to select the account, choose the one receiving OTP for login
    - Allow permission on that email to use just enabled __GMAIL API__
       - Click on `Continue` instead of __Back To Safety__
       - Then press `Continue` again
    - `token.json` will be generated in same folder as that of `credentials.json`
  
    > **Warning** `token.json` expires after sometime. So make sure to check that in your projects and keep refreshing it.

<div id="example"></div>

### Example

Now, we will create a script which will open ERP on your default browser with a logged in session.

1. Install the package.

   ```bash
   pip install iitkgp_erp_login
   ````
2. Make sure <a href="#erpcreds">erpcreds.py</a> & <a href="#token">token.json</a> exist in the same directory as that of the script we are about to create.

3. Create `open_erp.py` and append the following content into it.

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
4. Run the script
   ```bash
   python3 open_erp.py
   ```
