import jwt
import requests
from threading import Timer
import iitkgp_erp_login.erp as erp
from typing import Dict, Literal, Tuple
from datetime import datetime, timedelta

# Times (in seconds)
SESSION_TIMEOUT = 60 * 30
SESSION_CLEANUP = 60 * 60 * 6


class Session:
    def __init__(self):
        self.erp_session = requests.Session()
        self.session_token = None
        self.sso_token = None
        self.last_acccessed = datetime.now()


class SessionManager:
    _instance = None
    sessions: Dict[str, Session]

    def __init__(self, headers: Dict[str, str], secret_key: str) -> None:
        if not hasattr(self, 'initialized'):  # To ensure __init__ is called only once
            self.sessions = {}
            self.headers = headers
            self.secret_key = secret_key
            self.initialized = True
            self.__cleanup_sessions()

    def __generate_jwt(self, roll_number: str) -> str:
        payload = {
            'roll_number': roll_number,
            'exp': datetime.now() + timedelta(seconds=SESSION_TIMEOUT)  # Token expiration time
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def __verify_jwt(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['roll_number']
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def __create_session(self, roll_number: str) -> Tuple[str, Session]:
        token = self.__generate_jwt(roll_number)
        session = Session()
        self.sessions[token] = session
        return token, session

    def __get_session(self, token: str) -> Tuple[str, Session]:
        roll_number = self.__verify_jwt(token)
        session = self.sessions.get(token)
        if not session:
            raise ValueError(f"No ERP session found for token")

        # Update the last accessed time
        session.last_acccessed = datetime.now()

        return roll_number, session

    def __cleanup_sessions(self) -> None:
        now = datetime.now()
        expired_sessions = [token for token, session in self.sessions.items()
                            if now - session.last_acccessed > timedelta(seconds=SESSION_TIMEOUT)]

        for token in expired_sessions:
            self.end_session(token)

        Timer(SESSION_CLEANUP, self.__cleanup_sessions).start()

    def get_secret_question(self, roll_number: str) -> Tuple[str, str]:
        token, session = self.__create_session(roll_number)

        session_token = erp.get_sessiontoken(session.erp_session)
        session.session_token = session_token
        secret_question = erp.get_secret_question(
            self.headers, session.erp_session, roll_number)
        return secret_question, token

    def request_otp(self, token: str, password: str, secret_answer: str) -> None:
        roll_number, session = self.__get_session(token)

        login_details = erp.get_login_details(
            roll_number, password, secret_answer, session.session_token)

        erp.request_otp(self.headers, session.erp_session, login_details)

    def establish_erp_session(self, token: str, password: str, answer: str, otp: str) -> None:
        roll_number, session = self.__get_session(token)

        login_details = erp.get_login_details(
            ROLL_NUMBER=roll_number,
            PASSWORD=password,
            secret_answer=answer,
            sessionToken=session.session_token
        )
        login_details["email_otp"] = otp

        sso_token = erp.signin(
            self.headers, session.erp_session, login_details)
        session.sso_token = sso_token

    def end_session(self, token: str) -> None:
        if token in self.sessions:
            del self.sessions[token]

    def get_erp_session(self, token: str) -> Tuple[str, Session]:
        _ = self.__verify_jwt(token)
        session = self.sessions.get(token)
        if not session:
            raise ValueError(f"No ERP session found for token")

        # Update the last accessed time
        session.last_acccessed = datetime.now()

        return session.session_token, session.sso_token

    def request(self, token: str, url: str, method: Literal['GET', 'POST', 'PUT', 'DELETE'] = 'GET', **kwargs) -> requests.Response:
        _, session = self.__get_session(token)

        response = session.erp_session.request(
            method=method, url=url, **kwargs)

        return response
