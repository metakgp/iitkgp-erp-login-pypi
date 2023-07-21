import time
import base64
from googleapiclient.discovery import build
from iitkgp_erp_login.utils import generate_token

SUBJECT = "OTP for Sign In in ERP Portal of IIT Kharagpur"

def getMailID(service):
    query = f"subject:{SUBJECT}"
    results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
    messages = results.get("messages", [])
    
    if messages:
        message = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
        return message["id"]
    
    return None

def getOTP(OTP_CHECK_INTERVAL):
    creds = generate_token()
    service = build("gmail", "v1", credentials=creds)
    
    latest_mail_id = getMailID(service)
    while True:
        if (mail_id := getMailID(service)) != latest_mail_id:
            break
        time.sleep(OTP_CHECK_INTERVAL)
    
    mail = service.users().messages().get(userId="me", id=mail_id).execute()
    if "body" in mail["payload"]:
        body_data = mail["payload"]["body"]["data"]
        decoded_body_data = base64.urlsafe_b64decode(body_data).decode("utf-8")
        otp = [part for part in decoded_body_data.split() if part.isdigit()][-1]

        return otp
