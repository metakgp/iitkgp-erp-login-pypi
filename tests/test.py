import re
import requests
import time
import erpcreds as erpcreds
import iitkgp_erp_login.erp as erp

headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}
session = requests.Session()

# erp.login(headers, session, LOGGING=True)
erp.login(headers, session, ERPCREDS=erpcreds, LOGGING=True)
# erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=2, LOGGING=True)
# while True:
#     sessionToken, ssoToken = erp.login(headers, session, ERPCREDS=erpcreds, OTP_CHECK_INTERVAL=2, LOGGING=True, SESSION_STORAGE_FILE='.session')
#     r = session.get(erp.WELCOMEPAGE_URL)
    
#     status_code = r.status_code
#     if status_code == 200:
#         print(r.text)
#         content_length = r.headers.get("Content-Length")
#         break
