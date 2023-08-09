import os
import re
import ping3
import logging
import requests
import getpass
from typing import TypedDict

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup as bs
from iitkgp_erp_login.read_mail import getOTP
from iitkgp_erp_login.endpoints import *
from iitkgp_erp_login.utils import get_import_location, get_tokens_from_file, get_caller_file

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)
sessionToken = ""

class LoginDetails(TypedDict):
    user_id: str
    password: str
    answer: str
    sessionToken: str
    requestedUrl: str

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

def login(headers: dict[str, str], session: requests.Session, ERPCREDS: ErpCreds | None = None, OTP_CHECK_INTERVAL: float | None = None, LOGGING: bool | None = False, SESSION_STORAGE_FILE: str | None = None):
    global sessionToken
    ssoToken = None

    caller_file = get_caller_file()

    ROLL_NUMBER = ERPCREDS["ROLL_NUMBER"] if ERPCREDS else None
    PASSWORD = ERPCREDS["PASSWORD"] if ERPCREDS else None
    SECURITY_QUESTIONS_ANSWERS = ERPCREDS["SECURITY_QUESTIONS_ANSWERS"] if ERPCREDS else None

    token_file = f"{get_import_location(caller_file)}/{SESSION_STORAGE_FILE}" if SESSION_STORAGE_FILE else ""

    if SESSION_STORAGE_FILE: sessionToken, ssoToken = read_session_token_from_file(token_file=token_file, log=LOGGING)

    if ssoToken and ssotoken_valid(ssoToken):
        logging.info(" [SSOToken STATUS] >> Valid <<") if LOGGING else None
        session.cookies.set('ssoToken', ssoToken, domain='erp.iitkgp.ac.in')
    else:
        logging.info(" [SSOToken STATUS] >> Not Valid <<") if LOGGING and os.path.exists(token_file) else None

        if not ROLL_NUMBER: ROLL_NUMBER = input("Enter you Roll Number: ")
        if not PASSWORD: PASSWORD = getpass.getpass("Enter your ERP password: ")

        try:
            sessionToken = get_session_token(session=session)
            logging.info(" Generated sessionToken") if LOGGING else None
        except (requests.exceptions.RequestException, KeyError) as e:
            raise ErpLoginError(f"Failed to generate session token: {str(e)}")

        try:
            secret_question = get_secret_question(session=session, roll_number=ROLL_NUMBER, headers=headers)
            logging.info(" Fetched Security Question") if LOGGING else None

            if SECURITY_QUESTIONS_ANSWERS:
                secret_answer = SECURITY_QUESTIONS_ANSWERS[secret_question]
            else:
                print ("Your secret question: " + secret_question)
                secret_answer = getpass.getpass("Enter the answer to the secret question: ")

        except (requests.exceptions.RequestException, KeyError) as e:
            raise ErpLoginError(f"Failed to fetch Security Question: {str(e)}")

        login_details = {
            'user_id': ROLL_NUMBER,
            'password': PASSWORD,
            'answer': secret_answer,
            'sessionToken': sessionToken,
            'requestedUrl': HOMEPAGE_URL,
        }

        if not ping3.ping("iitkgp.ac.in"):
            try:
                r = session.post(OTP_URL, data={'typeee': 'SI', 'loginid': ROLL_NUMBER, 'pass': PASSWORD}, headers=headers)
                logging.info(" Requested OTP") if LOGGING else None
            except requests.exceptions.RequestException as e:
                raise ErpLoginError(f"Failed to request OTP: {str(e)}")

            if OTP_CHECK_INTERVAL != None:
                    try:
                        logging.info(" Waiting for OTP...") if LOGGING else None
                        otp = getOTP(OTP_CHECK_INTERVAL)
                        logging.info(" Received OTP") if LOGGING else None
                    except Exception as e:
                        raise ErpLoginError(f"Failed to receive OTP: {str(e)}")
            else:
                otp = input("Enter the OTP sent to your registered email address: ").strip()

            login_details['email_otp'] = otp
        else:
            logging.info(" OTP is not required :yay") if LOGGING else None

        try:
            ssoToken = erp_login(session=session, login_details=login_details, headers=headers, log=LOGGING)
        except e:
            raise e

        if SESSION_STORAGE_FILE:
            write_session_token(token_file=token_file, ssoToken=ssoToken, sessionToken=sessionToken)
            logging.info(" Stored tokens in the file") if LOGGING else None

    return sessionToken, ssoToken

