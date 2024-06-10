import erp 
import requests

headers = {
   'timeout': '20',
   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

session = requests.Session()


try :
  erp.login(headers,session, LOGGING=True)

except Exception as e:
    print("Error :"+ str(e))
      
