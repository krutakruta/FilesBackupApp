import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from Model.Clouds.google_drive_cloud import GoogleDriveCloud


# If modifying these scopes, delete the file token.pickle.
from Model.model_exceptions import ProgramException

SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob")
            creds = flow.run_console(f"Перейдите по ссылке для авторизации: {flow.authorization_url()[0]}",
                                     "Введите код авторизации: ")
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=30, fields="nextPageToken, files(id, name)").execute()
    file_metadata = {
        "name": "1.txt",
        "parents": []
    }
    media = MediaFileUpload("C:/kartinki/1.txt")
    r = service.files().create(body=file_metadata, media_body=media).execute()
    print(r)


def smain():
    d = GoogleDriveCloud(None)
    d.client_id = "57753386d6445-l9jiqaas7ehmo3uihiffvo83hd499fbf.apps.googleusercontent.com"
    d.client_secret = "B4h8o9fXlKYKE_y7RsJJavdd"
    d.authorize()
    print(d.xxx())


if __name__ == '__main__':
    main()






















