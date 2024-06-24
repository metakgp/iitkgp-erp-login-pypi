from math import log
import requests
import jwt as jwt_gen
from threading import Timer
import iitkgp_erp_login.erp as erp
from typing import Dict, Literal, Tuple
from datetime import datetime, timedelta

# In seconds
SESSION_TIMEOUT = 60 * 30
SESSION_CLEANUP = 60 * 60 * 6


class UserSession:
    def __init__(self):
        self.erp_session = requests.Session()
        self.session_token = None
        self.sso_token = None
        self.last_acccessed = datetime.now()


class SessionManager:
    def __init__(self, headers: Dict[str, str], jwt_secret_key: str) -> None:
        self.user_sessions_dict: Dict[str, UserSession] = {}
        self.headers = headers
        self.jwt_secret_key = jwt_secret_key
        self.__cleanup_sessions()

    def __generate_jwt(self, roll_number: str) -> str:
        payload = {
            'roll_number': roll_number,
            'exp': datetime.now() + timedelta(seconds=SESSION_TIMEOUT)  # Token expiration time
        }
        jwt = jwt_gen.encode(payload, self.jwt_secret_key, algorithm='HS256')
        return jwt

    def __verify_jwt(self, jwt: str) -> str:
        try:
            payload = jwt_gen.decode(
                jwt, self.jwt_secret_key, algorithms=['HS256'])
            return payload['roll_number']
        except jwt_gen.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt_gen.InvalidTokenError:
            raise ValueError("Invalid jwt")

    def __create_session(self, roll_number: str) -> Tuple[str, UserSession]:
        jwt = self.__generate_jwt(roll_number)
        user_session = UserSession()
        self.user_sessions_dict[jwt] = user_session
        return jwt, user_session

    def __get_session(self, jwt: str) -> Tuple[str, UserSession]:
        roll_number = self.__verify_jwt(jwt)
        user_session = self.user_sessions_dict.get(jwt)
        if not user_session:
            raise ValueError(f"User was loggeed out. Log-in again")

        # Update the last accessed time
        user_session.last_acccessed = datetime.now()

        return roll_number, user_session

    def __cleanup_sessions(self) -> None:
        current_time = datetime.now()
        expired_sessions = [jwt for jwt, session in self.user_sessions_dict.items()
                            if current_time - session.last_acccessed > timedelta(seconds=SESSION_TIMEOUT)]

        for jwt in expired_sessions:
            self.end_session(jwt)

        Timer(SESSION_CLEANUP, self.__cleanup_sessions).start()

    def get_erp_session(self, jwt: str) -> Tuple[str, str]:
        _, user_session = self.__get_session(jwt)

        return user_session.session_token, user_session.sso_token

    def end_session(self, jwt: str) -> None:
        if jwt in self.user_sessions_dict:
            del self.user_sessions_dict[jwt]

    def get_secret_question(self, roll_number: str, log: bool = True) -> Tuple[str, str]:
        jwt, user_session = self.__create_session(roll_number)

        user_session.session_token = erp.get_sessiontoken(
            user_session.erp_session, log)
        secret_question = erp.get_secret_question(
            self.headers, user_session.erp_session, roll_number, log)

        return secret_question, jwt

    def request_otp(self, jwt: str, password: str, secret_answer: str, log: bool = True) -> None:
        roll_number, user_session = self.__get_session(jwt)

        login_details = erp.get_login_details(
            roll_number, password, secret_answer, user_session.session_token)

        erp.request_otp(self.headers, user_session.erp_session, login_details, log)

    def login(self, jwt: str, password: str, secret_answer: str, otp: str, log: bool = True) -> None:
        roll_number, user_session = self.__get_session(jwt)

        login_details = erp.get_login_details(
            ROLL_NUMBER=roll_number,
            PASSWORD=password,
            secret_answer=secret_answer,
            sessionToken=user_session.session_token
        )
        login_details["email_otp"] = otp

        user_session.sso_token = erp.signin(
            self.headers, user_session.erp_session, login_details, log)

    def request(self, jwt: str, url: str, method: Literal['GET', 'POST', 'PUT', 'DELETE'] = 'GET', **kwargs) -> requests.Response:
        _, user_session = self.__get_session(jwt)

        try:
            response = user_session.erp_session.request(
                method=method, url=url, **kwargs)

            return response
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Failed to request ERP endpoint ({url}): {str(e)}")
