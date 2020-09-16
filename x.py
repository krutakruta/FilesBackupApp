import yadisk
import yandex_oauth
import webbrowser
import requests


def main():
    y = yadisk.YaDisk()
    y.id = "dbb2831b0635426e8e6ce2eb5433a1f7"
    y.secret = "a0da8ef5868f437a89aa6de798e21980"
    webbrowser.open(y.get_code_url(), new=1, autoraise=True)
    token = y.get_token(code=input())
    y.token = token["access_token"]
    for i in y.listdir("/тест", fields=["name", "resource_id", "path"]):
        print(f"name = {i.name}, path = {i.path}, id = {i.resource_id}")



    # port = 8080
    # host = "localhost"
    # success_message = "крута"
    # wsgi_app = _RedirectWSGIApp(success_message)
    # local_server = wsgiref.simple_server.make_server(
    #     host, port, wsgi_app, handler_class=wsgiref.simple_server.WSGIRequestHandler)
    # webbrowser.open(y.get_auth_url(type="token"), new=1, autoraise=True)
    # local_server.handle_request()
    # authorization_response = wsgi_app.last_request_uri.replace(
    #     'http', 'https')



class A:
    def __init__(self):
        self.a = "sss"


if __name__ == "__main__":
    main()





























# import pickle
# import os.path
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from Model.BackupDestination.google_drive_destination import GoogleDriveDestination
#
#
# # If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
#
#
# def main():
#     """Shows basic usage of the Drive v3 API.
#     Prints the names and ids of the first 10 files the user has access to.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('drive', 'v3', credentials=creds)
#
#     # Call the Drive v3 API
#     results = service.files().list(
#         pageSize=30, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#     x = service.files().get('0AIeEoT6Js27gUk9PVA').execute()
#     print(x)
#     return
#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(u'{0} ({1})'.format(item['name'], item['id']))
#
#
# def smain():
#     d = GoogleDriveDestination(None)
#     d.client_id = "577533866445-l9jiqaas7ehmo3uihiffvo83hd499fbf.apps.googleusercontent.com"
#     d.client_secret = "B4h8o9fXlKYKE_y7RsJJavdd"
#     d.authorize()
#     print(d.xxx())
#
#
# if __name__ == '__main__':
#     smain()
