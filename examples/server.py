import logging
import requests
import iitkgp_erp_login.erp as erp
import iitkgp_erp_login.utils as erp_utils
from flask import Flask, request, jsonify

app = Flask(__name__)

headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}


class ErpResponse:
    def __init__(self, success: bool, message: str = None, data: dict = None, status_code: int = 200):
        self.success = success
        self.message = message
        self.data = data or {}
        self.status_code = status_code

        if not success:
            logging.error(f" {message}")

    def to_dict(self):
        response = {
            "status": "success" if self.success else "error",
            "message": self.message
        }
        if self.data:
            response.update(self.data)
        return response

    def to_response(self):
        return jsonify(self.to_dict()), self.status_code


@app.route("/secret-question", methods=["POST"])
def get_secret_question():
    try:
        data = request.form
        roll_number = data.get("roll_number")
        if not roll_number:
            return ErpResponse(False, "Roll Number not provided", status_code=400).to_response()

        session = requests.Session()
        secret_question = erp.get_secret_question(headers=headers, session=session, roll_number=roll_number, log=True)
        sessionToken = erp_utils.get_cookie(session, 'JSESSIONID')

        return ErpResponse(True, message="ERP Login Completed!", data={
            "SECRET_QUESTION": secret_question,
            "SESSION_TOKEN": sessionToken
        }).to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


@app.route("/request-otp", methods=["POST"])
def request_otp():
    try:
        sessionToken = request.headers["Session-Token"]
        if not sessionToken:
            return ErpResponse(False, "Session-Token header not found", status_code=400).to_response()

        data = request.form
        roll_number = data.get("roll_number")
        password = data.get("password")
        secret_answer = data.get("secret_answer")
        if not all([roll_number, password, secret_answer]):
            return ErpResponse(False, "Missing roll_number or password or secret answer", status_code=400).to_response()

        session = requests.Session()
        erp_utils.set_cookie(session, 'JSESSIONID', sessionToken)
        login_details = erp.get_login_details(
            ROLL_NUMBER=roll_number,
            PASSWORD=password,
            secret_answer=secret_answer,
            sessionToken=sessionToken
        )
        erp.request_otp(headers=headers, session=session, login_details=login_details, log=True)

        return ErpResponse(True, message="OTP has been sent to your connected email accounts").to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()


@app.route("/login", methods=["POST"])
def login():
    try:
        sessionToken = request.headers["Session-Token"]
        if not sessionToken:
            return ErpResponse(False, "Session-Token header not found", status_code=400).to_response()

        data = request.form
        roll_number = data.get("roll_number")
        password = data.get("password")
        secret_answer = data.get("secret_answer")
        otp = data.get("otp")
        if not all([roll_number, password, secret_answer, otp]):
            return ErpResponse(False, "Missing roll_number or password or secret answer or otp", status_code=400).to_response()

        login_details = erp.get_login_details(
            ROLL_NUMBER=roll_number,
            PASSWORD=password,
            secret_answer=secret_answer,
            sessionToken=sessionToken
        )
        login_details["email_otp"] = otp

        session = requests.Session()
        erp_utils.set_cookie(session, 'JSESSIONID', sessionToken)
        ssoToken = erp.signin(headers=headers, session=session, login_details=login_details, log=True)

        return ErpResponse(True, data={
            "ssoToken": ssoToken
        }).to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()

@app.route("/timetable", methods=["POST"])
def timetable():
    try:
        ssoToken = request.headers["SSO-Token"]
        if not ssoToken:
            return ErpResponse(False, "SSO-Token header not found", status_code=400).to_response()

        ERP_TIMETABLE_URL = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
        data = {
            "ssoToken": ssoToken,
            "module_id": '16',
            "menu_id": '40',
        }

        session = requests.Session()
        erp_utils.populate_session_with_login_tokens(session, ssoToken)
        r = erp_utils.request(session, method='POST', url=ERP_TIMETABLE_URL, headers=headers, data=data)

        return ErpResponse(True, data={
            "status_code": r.status_code,
            "content": r.text
        }).to_response()
    except Exception as e:
        return ErpResponse(False, str(e), status_code=500).to_response()