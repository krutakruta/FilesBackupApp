from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from Model.BackupDestination.i_backup_destination import IBackupDestination
from Utilities.useful_functions import check_type_decorator



class GoogleDriveDestination(IBackupDestination):
    def __init__(self, name="GoogleDrive"):
        self.name = name
        self._include_flag = True
        self._credentials = self._create_credentials()
        self._scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        self._service = None

    def is_ready_to_authorize(self):
        return (self._credentials["installed"]["client_id"] and
                self._credentials["installed"]["client_secret"])

    def authorize(self):
        if self.is_ready_to_authorize():
            creds = InstalledAppFlow.from_client_config(
                self._credentials, self._scopes)\
                .run_local_server(port=0)
            self._service = build("drive", "v3", credentials=creds)

    def get_files_list(self):
        return self._service.files().list(
            pageSize=30, fields="nextPageToken, files(id, name)").execute()

    @property
    def client_id(self):
        return self._credentials["installed"]["client_id"]

    @property
    def client_secret(self):
        return self._credentials["installed"]["client_secret"]

    @property
    def description(self):
        return self.name

    @property
    def type_description(self):
        return "Google drive облако"

    @property
    def include(self):
        return self._include_flag

    @client_id.setter
    @check_type_decorator(str)
    def client_id(self, value):
        self._credentials["installed"]["client_id"] = value

    @client_secret.setter
    @check_type_decorator(str)
    def client_secret(self, value):
        self._credentials["installed"]["client_secret"] = value

    @include.setter
    @check_type_decorator(bool)
    def include(self, value):
        self._include_flag = value

    def _create_credentials(self):
        return {"installed": {
            "client_id": None,
            "client_secret": None,
            "project_id": "angular-land-288207",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":
                "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }}
