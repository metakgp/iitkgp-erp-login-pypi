from flask import Flask, request, jsonify
from flask_cors import CORS
from iitkgp_erp_login import session_manager


app = Flask(__name__)
CORS(app, support_credentials=True)

# Initialize the SessionManager instance
session_manager = session_manager.SessionManager()


@app.route("/secret-question", methods=["POST"])
def get_secret_question():
    try:
        data = request.form
        roll = data.get("roll")
        if not roll:
            return jsonify({"status": "error", "message": "Missing roll number"}), 400
        token = session_manager.generate_jwt(roll)
        secret_question = session_manager.get_secret_question(token)
        return jsonify({"status": "success", "secret_question": secret_question,"token": token}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/request-otp", methods=["POST"])
def request_otp():
    try:
        token = request.headers.get("Authorization")
        passw = request.form.get("pass")
        secret_answer = request.form.get("secret_answer")
        
        if not all([token, passw, secret_answer]):
            return jsonify({"status": "error", "message": "Missing token, password, or secret answer"}), 400
        
        session_manager.request_otp(token, passw, secret_answer)
        return jsonify({"status": "success", "message": "OTP sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route("/login", methods=["POST"])
def login_and_download_ics():
    try:
        token = request.headers.get("Authorization")
        password = request.form.get("password")
        answer = request.form.get("secret_answer")
        email_otp = request.form.get("email_otp")
        
        if not all([token, email_otp]):
            return jsonify({"status": "error", "message": "Missing token or email OTP"}), 400
        
        session_manager.establish_erp_session(token=token,answer=answer,email_otp= email_otp,password=password)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
        