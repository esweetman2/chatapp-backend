# import datetime
# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2 import service_account
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# class GoogleService:
#     def __init__(self):
#         self.SERVICE_ACCOUNT_CREDS = "C:\\Users\\eswee\\chatapp-backend\\Backend\\Agents\\Tools\\home-agent-473522-2fae62ed615d.json"
#         self.SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

#     def get_creds(self):
        
#         creds = None
#         if os.path.exists(self.SERVICE_ACCOUNT_CREDS):
#             creds = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_CREDS, scopes=self.SCOPES)
#         return creds