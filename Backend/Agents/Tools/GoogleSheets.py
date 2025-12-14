import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import gspread
load_dotenv()

class GoogleSheets:
    def __init__(self):
        self.SERVICE_ACCOUNT_CREDS = os.getenv("SERVICE_ACCOUNT_CREDS")
        self.SCOPES = [ "https://www.googleapis.com/auth/spreadsheets.readonly"]

    def get_creds(self):
        creds = None
        if os.path.exists(self.SERVICE_ACCOUNT_CREDS):
            creds = gspread.service_account(filename=self.SERVICE_ACCOUNT_CREDS)
        
        return creds
    
    def read_google_sheet(self,google_sheet_name, worksheet):
        try:
            creds = self.get_creds()
            # gs_auth = gspread.authorize(creds)
            # Authenticate using the service account file
            # gc = gspread.service_account(filename=self.SERVICE_ACCOUNT_CREDS)

            # Open the Google Sheet by its name
            sh = creds.open(google_sheet_name)

            # Select a worksheet
            worksheet = sh.worksheet(worksheet)

            # Fetch all data as a list of dictionaries (assuming first row is headers)
            data = worksheet.get_all_records(expected_headers=[""])

            # Convert the data into a pandas DataFrame for easy manipulation
            # df = pd.DataFrame(data)

            return data

        except Exception as e:
            return f"An error occurred: {e}"

# if __name__ == '__main__':
#     _GoogleService = GoogleSheets()
#     google_sheet = _GoogleService.read_google_sheet(google_sheet_name="Zermatt Honeymoon", worksheet="Schedule")
#     print(google_sheet)