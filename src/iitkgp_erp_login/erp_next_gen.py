import re
import ping3
import logging
import requests
from typing import TypedDict

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup as bs
from iitkgp_erp_login.endpoints import *
from iitkgp_erp_login.utils import get_tokens_from_file

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)
sessionToken = ""

class LoginDetails(TypedDict):
    user_id: str
    password: str
    answer: str
    sessionToken: str
    requestedUrl: str
    email_otp: str

class ErpCreds(TypedDict):
    ROLL_NUMBER: str
    PASSWORD: str
    SECURITY_QUESTIONS_ANSWERS: dict[str, str]

class ErpLoginError(Exception):
    pass

def ssotoken_valid(ssoToken: str):
    """Checks whether an SSO token is valid."""
    response = requests.get(f"{HOMEPAGE_URL}?ssoToken={ssoToken}")
    content_type = str(response.headers).split(',')[-1].split("'")[-2]
    return content_type == 'text/html;charset=UTF-8'

def session_alive(session: requests.Session):
    """Checks if a session is alive."""
    r = session.get(WELCOMEPAGE_URL)
    return r.status_code == 404

def get_secret_question(session: requests.Session, roll_number: str, headers: dict[str, str]):
    """Fetches the secret question given the roll number."""
    r = session.post(SECRET_QUESTION_URL, data={'user_id': roll_number}, headers=headers)

    return r.text

def read_session_token_from_file(token_file: str, log: bool):
    """Reads session tokens from a token file if it exists."""
    try:
        sessionToken, ssoToken = get_tokens_from_file(token_file)
        if log: logging.info(" Retrieved tokens from the file")

        return sessionToken, ssoToken
    except (FileNotFoundError, IOError):
        if log: logging.error(f" Token file doesn't exist")

def get_session_token(session: requests.Session):
    """Gets the session token from the response of an HTTP request."""
    r = session.get(HOMEPAGE_URL)
    soup = bs(r.text, 'html.parser')

    return soup.find(id='sessionToken')['value']

def is_otp_required():
    """Checks whether the request is run from the campus network (OTP not required) or not."""
    return not ping3.ping("iitkgp.ac.in")

def request_otp(
    session: requests.Session,
    headers: dict[str, str],
    roll_number: str,
    password: str,
    log: bool
):
    """Requests an OTP to be sent."""
    session.post(OTP_URL, data={'typeee': 'SI', 'loginid': roll_number, 'pass': password}, headers=headers)

    if log: logging.info(" Requested OTP")

def erp_login(session: requests.Session, login_details: LoginDetails, headers: dict[str, str], log: bool):
    """Logs into the ERP for the given session."""
    try:
        r = session.post(LOGIN_URL, data=login_details, headers=headers)
        ssoToken = re.search(r'\?ssoToken=(.+)$', r.history[1].headers['Location'])

        if ssoToken is None:
            raise ErpLoginError(f"Failed to generate ssoToken: {str(e)}")

        if log: logging.info(" Generated ssoToken")
    except (requests.exceptions.RequestException, IndexError) as e:
        raise ErpLoginError(f"ERP login failed: {str(e)}")

    if log: logging.info(" ERP login completed!")
    return ssoToken.group(1)

def write_session_token(token_file: str, sessionToken: str, ssoToken: str):
    """Writes session tokens to the token file if present."""
    with open(token_file, "w") as file:
        file.write(sessionToken + "\n")
        file.write(ssoToken + "\n")