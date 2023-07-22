# ERP Login Module

Tired of the tedious ERP login process? Wanted to automate some ERP workflow but stuck at login? <br>
🚀 Introducing **iitkgp-erp-login**: Your Ultimate ERP Login Automation Module for _IIT-KGP_ ! 🚀

Key Features:

- Seamless Credentials & OTP Handling
- Effortless Session & ssoToken Management
- Smart Token Storage for Efficiency

> **Note** This package is not officially affiliated with IIT Kharagpur.

<details>
  <summary>Table of Contents</summary>

- <a href="#endpoints">Endpoints</a>
	- <a href="#endpoints-about">About</a>
	- <a href="#endpoints-usage">Usage</a>
- <a href="#login">Login</a>
	- <a href="#login-input">Input</a>
	- <a href="#login-output">Output</a>
	- <a href="#login-usage">Usage</a>
- <a href="#session-alive">Session status check</a>
	- <a href="#session-alive-input">Input</a>
	- <a href="#session-alive-output">Output</a>
	- <a href="#session-alive-usage">Usage</a>
- <a href="#ssotoken-alive">SSOToken status check</a>
	- <a href="#ssotoken-alive-input">Input</a>
	- <a href="#ssotoken-alive-output">Output</a>
	- <a href="#ssotoken-alive-usage">Usage</a>
- <a href="#tokens-from-file">Get tokens from file</a>
- <a href="#example">Example</a>

</details>

<div id="endpoints"></div>

## Endpoints

The [endpoints.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/endpoints.py) file includes all the necessary endpoints for the ERP login workflow.

<div id="endpoints-about"></div>

### About

- `HOMEPAGE_URL`: The URL of the ERP homepage/loginpage.
- `SECRET_QUESTION_URL`: The URL for retrieving the secret question for authentication.
- `OTP_URL`: The URL for requesting the OTP (One-Time Password) for authentication.
- `LOGIN_URL`: The URL for ERP login.
- `WELCOMEPAGE_URL`: The URL of the welcome page, which is accessible only when the user is **NOT** logged in, and behaves exactly like the `HOMEPAGE_URL`. However, when the user is logged in, it returns a `404` error.

<div id="endpoints-usage"></div>

### Usage

```python
from iitkgp_erp_login.endpoints import *

print(HOMEPAGE_URL)
# Output: https://erp.iitkgp.ac.in/IIT_ERP3/

print(LOGIN_URL)
# Output: https://erp.iitkgp.ac.in/SSOAdministration/auth.htm
```

<div id="login"></div>

## Login

ERP login workflow is implemented in `login(headers, session, ERPCREDS=None, OTP_CHECK_INTERVAL=None, LOGGING=False, SESSION_STORAGE_FILE=None)` function in [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py). The input and output specifications for the function are mentioned below.

<div id="login-input"></div>

### Input

The function requires following _compulsory_ arguments:

1. `headers`: Headers for the post requests.

   ```python
   headers = {
      'timeout': '20',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
   }
   ```

2. `session`: A [requests.Session()](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) object, to persist the session parameters throughout the workflow.

   ```python
   import requests

   session = requests.Session()
   ```

The function can also be provided with these _optional_ arguments:

<div id="erpcreds"></div>

1. `ERPCREDS`: ERP Login Credentials python file, which is imported into main python file.<br>
    | Default Value | `None` |
    |---|---|
    | NOT Specified | The user is prompted to enter their credentials manually |
    | Specified (`ERPCREDS=erpcreds`) | The credentials are retrieved from the `erpcreds.py` file |

    > **Note** Here, `credentials` refer to the roll number, password, and security question.

    <details>
      <summary><b>Prerequisites - ERP credentials file</b></summary>

    - This file **MUST** be present in the same directory as the script where `iitkgp_erp_login` module is being imported.
    - Create a `.py` file with your ERP credentials stored in it. Please follow the instructions below to create this file:
      - You can choose any valid name for the file, adhering to Python's naming conventions.
      - **Do not change the variable names**. Copy the format provided below & update the values inside the `double quotes` (").

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

    </details>

<div id="token"></div>

2. `OTP_CHECK_INTERVAL`: The interval (in _seconds_) after which the API continuously checks for new OTP emails.
    | Default Value | `None` |
    |---|---|
    | NOT Specified | The user will be prompted to manually enter the received OTP |
    | Specified (`OTP_CHECKINTERVAL=2`) | The OTP will be automatically fetched and checked every `2 seconds` |
  
    <details>
      <summary><b>Prerequisites - Token for GMail enabled googleapi</b></summary>

    The token file **MUST** be present in the same directory as the script where `iitkgp_erp_login` module is being imported.

    1. Follow the steps in the [Gmail API - Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) guide to obtain `credentials.json` file.
       > **Note** The `credentials.json` file is permanent unless you manually delete its reference in your Google Cloud Console.

    2. To generate the `token.json` file, follow the steps below:
        - Import this module

          ```bash
          pip install iitkgp-erp-login
          ```

        - Execute following command:

          ```bash
          python3 -c "from iitkgp_erp_login.utils import generate_token; generate_token()"
          ```

        - A browser window will open, prompting you to select the Google account associated with receiving OTP for login.
        - Grant permission to the selected email address to utilize the newly enabled **Gmail API**.
           - Click on `Continue` instead of **Back To Safety**
           - Then, press `Continue` again
        - The `token.json` file will be generated in the same folder as the `credentials.json` file

        > **Warning** The `token.json` file has an expiration time, so it's important to periodically check and refresh it in your projects to ensure uninterrupted access.

3. `LOGGING`: Toggles **comprehensive logging**.
    | Default value | `False` |
    |---|---|
    | NOT Specified | No Logging |
    | Specified (`LOGGING=True`) | Logs every step in an exhaustive manner |

4. `SESSION_STORAGE_FILE`: A file where `sessionToken` and `ssoToken` -  collectively referred to as "session tokens" here  - are stored for direct usage.
    | Default value | `None` |
    |---|---|
    | NOT Specified | The session tokens will not be stored in a file |
    | Specified (`SESSION_STORAGE_FILE=".session"`) | The session tokens will be stored in `.session` file for later direct usage |

    > **Note** The approximate expiry time for `ssoToken` is _~30 minutes_ and that of `session` object is _~2.5 hours_

<div id="login-output"></div>

### Output

1. The function returns the following, in the order of occurrence as here (`return sessionToken, ssoToken`):
   1. [sessionToken](https://en.wikipedia.org/wiki/Session_ID)
   2. [ssoToken](https://en.wikipedia.org/wiki/Single_sign-on)
2. It also modifies the `session` object, which now includes parameters for the logged-in session. This `session` object can be utilized for further navigation within the ERP system.

<div id="login-usage"></div>

### Usage

It is recommended to use the `login` function in the following manner (optional arguments are _your_ choice):

```python
# Importing the erp.py file
import iitkgp_erp_login.erp as erp

# Using the login function inside erp.py
sessionToken, ssoToken = erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=2, LOGGING=True, SESSION_STORAGE_FILE=".session")
```

Here are some examples combining all the aspects we have discussed so far about the `login` function:

```python
import requests
import erpcreds
import iitkgp_erp_login.erp as erp

headers = {
   'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}
session = requests.Session()

sessionToken, ssoToken = erp.login(headers, session)
# Credentials: Manual | OTP: Manual | Logging: No | TokenStorage: No

sessionToken, ssoToken = erp.login(headers, session, ERPCREDS=erpcreds)
# Credentials: Automatic - from erpcreds.py | OTP: Manual | Logging: No | TokenStorage: No

sessionToken, ssoToken = erp.login(headers, session, OTP_CHECK_INTERVAL=2)
# Credentials: Manual | OTP: Automatic - checked every 2 seconds | Logging: No | TokenStorage: No

sessionToken, ssoToken = erp.login(headers, session, LOGGING=True)
# Credentials: Manual | OTP: Manual | Logging: Yes | TokenStorage: No

sessionToken, ssoToken = erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=5)
# Credentials: Automatic - from erpcreds.py | OTP: Automatic - checked every 5 seconds | Logging: No | TokenStorage: No

sessionToken, ssoToken = erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=2, LOGGING=True)
# Credentials: Automatic - from erpcreds.py | OTP: Automatic - checked every 2 seconds | Logging: Yes | TokenStorage: No

sessionToken, ssoToken = erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=2, SESSION_STORAGE_FILE='.session')
# Credentials: Automatic - from erpcreds.py | OTP: Automatic - checked every 2 seconds | Logging: No | TokenStorage: in .session file

sessionToken, ssoToken = erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=2, LOGGING=True, SESSION_STORAGE_FILE='.session')
# Credentials: Automatic - from erpcreds.py | OTP: Automatic - checked every 2 seconds | Logging: Yes | TokenStorage: in .session file
```

> **Note** These are just examples of how to use the _login_ function, not satisfying the prerequisites.
>> Some arguments of `login()` have their own prerequisites that must be satisfied in order to use them. See <a href="#login-input">"Input" section of login</a> for complete details.

<div id="session-alive"></div>

## Session status check

The logic for checking the status of the session is implemented in the `session_alive(session)` function in [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py). This function determines whether the given session is valid/alive or not. The input and output specifications for the function are mentioned below.

<div id="session-alive-input"></div>

### Input

The function requires following argument:

- `session`: [requests.Session()](https://docs.python-requests.org/en/latest/_modules/requests/sessions/) object, to persist the session parameters throughout the workflow.

  ```python
  import requests

  session = requests.Session()
  ```

<div id="session-alive-output"></div>

### Output

The `session_alive(session)` function returns the status of the session as a boolean value:
| Status | Return Value |
| ------ | :------------: |
| Valid (`Alive`) | `True` |
| Not Valid (`Dead`) | `False` |

<div id="session-alive-usage"></div>

### Usage

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

import erpcreds
# Importing erpcreds.py, which contains ERP credentials

import iitkgp_erp_login.erp as erp

headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}
session = requests.Session()

print("Logging into ERP for:", creds.ROLL_NUMBER)

while True:
    if not erp.session_alive(session):
        erp.login(headers, session, ERPCREDS=erpcreds, LOGGING=True)
    else:
        print("Session is alive.")

    time.sleep(2)
```

<div id="ssotoken-alive"></div>

## SSOToken status check

The logic for checking the validity of the ssoToken is implemented in the `ssotoken_valid(ssoToken)` function in [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py). The input and output specifications for the function are mentioned below.

<div id="ssotoken-alive-input"></div>

### Input

The function requires following argument:

- `ssoToken`: The second returned value from the `login` function.

  ```python # Importing the erp.py file
  import iitkgp_erp_login.erp as erp

  # Using the login function inside erp.py - all others are optional arguments
  _, ssoToken = erp.login(headers, session)
  ```

<div id="ssotoken-alive-output"></div>

### Output

The `ssotoken_valid(ssoToken)` function returns the validity status of the ssotoken as a boolean value:
| Status | Return Value |
| ------ | :------------: |
| Valid | `True` |
| Not Valid | `False` |

<div id="ssotoken-alive-usage"></div>

### Usage

It is recommended to use the `ssotoken_valid` function in the following manner:

```python
# Importing the erp.py file
import iitkgp_erp_login.erp as erp

# Using the ssotoken_valid function inside erp.py
print(erp.ssotoken_valid(ssoToken))
```

Here's an example combining all the aspects we have discussed so far about the `login` function and `ssotoken_valid` function. <br>
This code can be used to log in to the ERP system while storing the ssoToken. If the ssoToken remains valid, it can be used directly for subsequent logins, eliminating the need to re-authenticate each time:

```python
import webbrowser
import requests
import time

import creds
# Importing creds.py, which contains ERP credentials

import iitkgp_erp_login.erp as erp

headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}
session = requests.Session()
print("Logging into ERP for:", creds.ROLL_NUMBER)

if os.path.exists(".session"):
    with open(".session", "r") as file:
        ssoToken = file.read()
    if not erp.ssotoken_valid(ssoToken):
        _, ssoToken = erp.login(headers, session, ERPCREDS=creds, OTP_CHECK_INTERVAL=2, LOGGING=True)
        with open(".session", "w") as file:
            file.write(ssoToken)
else:
    _, ssoToken = erp.login(headers, session, ERPCREDS=creds, OTP_CHECK_INTERVAL=2, LOGGING=True)
    with open(".session", "w") as file:
        file.write(ssoToken)

logged_in_url = f"{HOMEPAGE_URL}?ssoToken={ssoToken}"
webbrowser.open(logged_in_url)
```

> **Note** This is merely a Proof of Concept example; this exact functionality has been integrated into the login function itself from version **2.1.0** onwards.

<div id="tokens-from-file"></div>

## Get tokens from file

The logic for retrieving tokens (`sessionToken` & `ssoToken`) from a file, created earlier by the module itself, is implemented in the `get_tokens_from_file(token_file)` function in [erp.py](https://github.com/proffapt/iitkgp-erp-login-pypi/blob/main/src/iitkgp_erp_login/erp.py). The input and output specifications for the function are mentioned below.

<table>
<tr>
<td> Input </td> 
<td> 

`token_file` - The file containing tokens. 

</td>
</tr>
<tr>
<td> Output </td>
<td>

`sessionToken, ssoToken`

</td>
</tr>
<tr>
<td> Usage </td>
<td>

```python
import iitkgp_erp_login.erp as erp

sessionToken, ssoToken = erp.get_tokens_from_file('.session_token')
# Here, '.session_token' is the name of file contianing session tokens.
# It must be as same as the value of 'SESSION_STORAGE_FILE', if used.
```

</td>
</tr>
</table>

<div id="example"></div>

## Example

Now, we will create a script that opens the ERP Homepage on your default browser with a logged-in session.

1. Install the package.

   ```bash
   pip install iitkgp-erp-login
   ```

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

   _, ssoToken = erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=2, LOGGING=True, SESSION_STORAGE_FILE=".session")

   logged_in_url = f"{HOMEPAGE_URL}?ssoToken={ssoToken}"
   webbrowser.open(logged_in_url)
   ```

4. Run the script.

   ```bash
   python3 open_erp.py
   ```
