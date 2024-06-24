import webbrowser
from flask_cors import CORS
from flask import Flask, request, jsonify
from iitkgp_erp_login import session_manager


app = Flask(__name__)
CORS(app)

secret_key = "top-secret-unhackable-key"
headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

# Initialize the SessionManager instance
session_manager = session_manager.SessionManager(
    secret_key=secret_key, headers=headers)


@app.route("/secret-question", methods=["POST"])
def get_secret_question():
    try:
        data = request.form

        roll_number = data.get("roll_number")
        if not roll_number:
            return jsonify({"status": "error", "message": "Missing roll number"}), 400

        secret_question, token = session_manager.get_secret_question(
            roll_number)

        return jsonify({"status": "success", "secret_question": secret_question, "token": token}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/request-otp", methods=["POST"])
def request_otp():
    try:
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"status": "error", "message": "Authentication token not provided"}), 401

        password = request.form.get("password")
        secret_answer = request.form.get("secret_answer")

        if not all([token, password, secret_answer]):
            return jsonify({"status": "error", "message": "Missing token, password, or secret answer"}), 400

        session_manager.request_otp(token, password, secret_answer)
        return jsonify({"status": "success", "message": "OTP sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"status": "error", "message": "Authentication token not provided"}), 401

        password = request.form.get("password")
        secret_answer = request.form.get("secret_answer")
        otp = request.form.get("otp")

        if not all([token, secret_answer, password, otp]):
            return jsonify({"status": "error", "message": "Missing token or OTP"}), 400

        session_manager.establish_erp_session(
            token=token, answer=secret_answer, otp=otp, password=password)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/logout", methods=["GET"])
def logout():
    try:
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"status": "error", "message": "Authentication token not provided"}), 401

        session_manager.end_session(token=token)

        return jsonify({"status": "success", "message": "You are logged out"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/timetable", methods=["POST"])
def timetable():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({"status": "error", "message": "Authentication token not provided"}), 401

    _, ssoToken = session_manager.get_erp_session(token=token)

    ERP_TIMETABLE_URL = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
    data = {
        "ssoToken": ssoToken,
        "module_id": '16',
        "menu_id": '40',
    }
    r = session_manager.request(
        token=token, method='POST', url=ERP_TIMETABLE_URL, headers=headers, data=data)
    return jsonify({"status_code": r.status_code}), 200
