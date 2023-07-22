import os
import sys
import inspect
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

def get_import_location(caller_file=None):
    if len(sys.argv) == 1 and sys.argv[0] == '-c':
        return os.getcwd()
    else:
        current_frame = inspect.currentframe()
        while current_frame.f_back:
            current_frame = current_frame.f_back
            frame_file = inspect.getframeinfo(current_frame).filename
            if caller_file == frame_file:
                break

        script_file_path = inspect.getframeinfo(current_frame).filename
        script_directory_path = os.path.dirname(script_file_path)

        return script_directory_path

def generate_token():
	if len(sys.argv) == 1 and sys.argv[0] == '-c':
		caller_file = None
	else:
		caller_file = inspect.getframeinfo(inspect.currentframe().f_back.f_back.f_back).filename
	token_path = os.path.join(get_import_location(caller_file), "token.json")
	credentials_path = os.path.join(get_import_location(caller_file), "credentials.json")
	scopes = [f"https://www.googleapis.com/auth/gmail.readonly"]	

	creds = None
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

		return creds
