import os
import pickle
import google.auth
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up the API credentials and scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Token file for storing user's authentication
TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'credentials.json'

def authenticate_google_account():
    """Handles the OAuth 2.0 authentication process for Google account."""
    credentials = None
    # If token.json exists, use it to get the credentials
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            credentials = pickle.load(token)
    
    # If there's no valid credentials, initiate OAuth flow
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save credentials to token.json for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(credentials, token)
    
    return credentials

def list_drive_files(credentials):
    """Lists the first 10 files from Google Drive."""
    try:
        service = build('drive', 'v3', credentials=credentials)
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        
        if not items:
            print('No files found.')
            return []
        else:
            return items
    
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def is_user_logged_in():
    """Check if the user is already logged in by checking token.json."""
    return os.path.exists(TOKEN_PATH)

def run_oauth_flow():
    """Runs the OAuth flow if the user is not logged in."""
    credentials = authenticate_google_account()
    return credentials

def login_with_google():
    """Handles logging in a user via Google OAuth."""
    credentials = authenticate_google_account()
    if credentials:
        print("User logged in successfully.")
        return credentials
    else:
        print("Failed to log in.")
        return None
    
import requests

import requests

def get_user_info(credentials):
    try:
        response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {credentials.token}"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to get user info:", response.text)
            raise Exception("Failed to get user info")
    except Exception as e:
        print(f"Error in get_user_info: {e}")
        raise


