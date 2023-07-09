import os
import re
import time
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def setup_api():
    # Set up API credentials
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

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    # Connect to the Gmail API
    return build("gmail", "v1", credentials=creds)

def get_mail_id():
    service = setup_api()  # API connection service

    # Search for emails with the specified subject and retrieve the latest email
    subject = "OTP for Sign In in ERP Portal of IIT Kharagpur"
    query = f"subject:{subject}"
    results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
    messages = results.get("messages", [])
    
    # Check whether there are any mails retrieved
    if messages:
        message = messages[0]
        mail_id = message["id"]
        
        return mail_id

    return None

def get_mail_data(mail_id):
    service = setup_api()
    mail = service.users().messages().get(userId="me", id=mail_id).execute() # Retrieve the email with the specified ID
    
    return mail

def get(OTP_WAIT_INTERVAL):
    latest_mail_id = get_mail_id()
    
    # Fetch the latest OTP email id
    while True:
        mail_id = get_mail_id()
        if mail_id != latest_mail_id:
            break
        
        time.sleep(OTP_WAIT_INTERVAL)
            
    # Get the latest OTP email body
    mail = get_mail_data(mail_id)
    if "body" in mail["payload"]:
        # Get the email body
        body_data = mail["payload"]["body"]["data"]
        decoded_body_data = base64.urlsafe_b64decode(body_data).decode("utf-8")
        # Extracting OTP
        otp = decoded_body_data.split()[-1]

        return otp
