import os
import re
import sys
import inspect
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup as bs
from iitkgp_erp_login.read_mail import getOTP
from iitkgp_erp_login.endpoints import *
from iitkgp_erp_login.utils import get_import_location

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)
sessionToken = ""

class ErpLoginError(Exception):
    pass


def login(headers, session, ERPCREDS=None, OTP_CHECK_INTERVAL=None, LOGGING=False, SESSION_STORAGE_FILE=None):
    global sessionToken
    ssoToken = None
    if len(sys.argv) == 1 and sys.argv[0] == '-c':
        caller_file = None
    else:
        caller_file = inspect.getframeinfo(inspect.currentframe().f_back).filename
    token_file = f"{get_import_location(caller_file)}/{SESSION_STORAGE_FILE}" if SESSION_STORAGE_FILE else ""
    if SESSION_STORAGE_FILE:
        try:
            sessionToken, ssoToken = get_tokens_from_file(token_file)
            logging.info(" Retrieved tokens from the file") if LOGGING else None
        except (FileNotFoundError, IOError):
            logging.error(f" Token file doesn't exist") if LOGGING else None

    if ssoToken and ssotoken_valid(ssoToken):
        logging.info(" [SSOToken STATUS] >> Valid <<") if LOGGING else None
        session.cookies.set('ssoToken', ssoToken, domain='erp.iitkgp.ac.in')
    else:
        logging.info(" [SSOToken STATUS] >> Not Valid <<") if LOGGING and os.path.exists(token_file) else None
        
        if ERPCREDS != None:
            ROLL_NUMBER = ERPCREDS.ROLL_NUMBER
            PASSWORD = ERPCREDS.PASSWORD
        else:
            import getpass
            ROLL_NUMBER = input("Enter you Roll Number: ")
            PASSWORD = getpass.getpass("Enter your ERP password: ")

        try:
            r = session.get(HOMEPAGE_URL)
            soup = bs(r.text, 'html.parser')
            sessionToken = soup.find(id='sessionToken')['value']
            logging.info(" Generated sessionToken") if LOGGING else None
        except (requests.exceptions.RequestException, KeyError) as e:
            raise ErpLoginError(f"Failed to generate session token: {str(e)}")
        
        try:
            r = session.post(SECRET_QUESTION_URL, data={'user_id': ROLL_NUMBER}, headers=headers)
            secret_question = r.text
            logging.info(" Fetched Security Question") if LOGGING else None

            if ERPCREDS != None:
                secret_answer = ERPCREDS.SECURITY_QUESTIONS_ANSWERS[secret_question]
            else:
                print ("Your secret question: " + secret_question)
                secret_answer = getpass.getpass("Enter the answer to the secret question: ")
        except (requests.exceptions.RequestException, KeyError) as e:
            raise ErpLoginError(f"Failed to fetch Security Question: {str(e)}")

        try:
            r = session.post(OTP_URL, data={'typeee': 'SI', 'loginid': ROLL_NUMBER, 'pass': PASSWORD}, headers=headers)
        except requests.exceptions.RequestException as e:
            raise ErpLoginError(f"Failed to request OTP: {str(e)}")
        
        login_details = {
            'user_id': ROLL_NUMBER,
            'password': PASSWORD,
            'answer': secret_answer,
            'sessionToken': sessionToken,
            'requestedUrl': HOMEPAGE_URL,
        }

        if r.status_code == 200:
            logging.info(" Requested OTP") if LOGGING else None
            
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
            r = session.post(LOGIN_URL, data=login_details, headers=headers)
            ssoToken = re.search(r'\?ssoToken=(.+)$', r.history[1].headers['Location'])
            if ssoToken is None:
                raise ErpLoginError(f"Failed to generate ssoToken: {str(e)}")
            ssoToken = ssoToken.group(1)
            logging.info(" Generated ssoToken") if LOGGING else None
        except (requests.exceptions.RequestException, IndexError) as e:
            raise ErpLoginError(f"ERP login failed: {str(e)}")

        logging.info(" ERP login completed!") if LOGGING else None

        if SESSION_STORAGE_FILE:
            with open(token_file, "w") as file:
                file.write(sessionToken + "\n")
                file.write(ssoToken + "\n")
            logging.info(" Stored tokens in the file") if LOGGING else None

    return sessionToken, ssoToken


def session_alive(session):
    r = session.get(WELCOMEPAGE_URL)
    return r.status_code == 404


def ssotoken_valid(ssoToken):
    response = requests.get(f"{HOMEPAGE_URL}?ssoToken={ssoToken}")
    content_type = str(response.headers).split(',')[-1].split("'")[-2]
    return content_type == 'text/html;charset=UTF-8'


def get_tokens_from_file(token_file):
    with open(token_file, "r") as file:
        lines = file.readlines()
        sessionToken = lines[0].strip() if len(lines) > 0 else None
        ssoToken = lines[1].strip() if len(lines) > 1 else None

    return sessionToken, ssoToken

