import os
import time
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SUBJECT = "OTP for Sign In in ERP Portal of IIT Kharagpur"

def setup_api():
    creds = None
    token_path = "token.json"
    credentials_path = "credentials.json"
    scopes = ["https://www.googleapis.com/auth/gmail.readonly"]

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
            creds = flow.run_local_server(port=0)

        if not os.path.exists(token_path):
            with open(token_path, "w") as token:
                token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def get_mail_id(service):
    query = f"subject:{SUBJECT}"
    results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
    messages = results.get("messages", [])
    
    if messages:
        message = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
        return message["id"]
    
    return None

def get(OTP_WAIT_INTERVAL):
    service = setup_api()
    latest_mail_id = get_mail_id(service)
    
    while True:
        if (mail_id := get_mail_id(service)) != latest_mail_id:
            break
        
        time.sleep(OTP_WAIT_INTERVAL)
    
    mail = service.users().messages().get(userId="me", id=mail_id).execute()
    
    if "body" in mail["payload"]:
        body_data = mail["payload"]["body"]["data"]
        decoded_body_data = base64.urlsafe_b64decode(body_data).decode("utf-8")
        otp = [part for part in decoded_body_data.split() if part.isdigit()][-1]

        return otp
