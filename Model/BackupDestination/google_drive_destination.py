from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from Model.BackupDestination.i_backup_destination import IBackupDestination
from Model.BackupElements\
    .i_google_drive_backupable import IGoogleDriveBackupable
from Model.model_exceptions import GoogleDriveIsNotReadyToAuthorize
from Utilities.useful_functions import check_type_decorator


class Graph:
    def __init__(self, data):
        self.data = data
        self.parents = []
        self.children = []


class GoogleDriveDestination(IBackupDestination):
    def __init__(self, args_provider, title="GoogleDrive", client_id=None, client_sec=None):
        self._title = title
        self._include_flag = True
        self._sub_path = "/"
        self._credentials = self._create_credentials(client_id, client_sec)
        self._scopes = ['https://www.googleapis.com/auth/drive']
        self._service = None
        self._args_provider = args_provider

    def ready_to_authorize(self):
        return (self._credentials["installed"]["client_id"] and
                self._credentials["installed"]["client_secret"])

    def authorize(self):
        if not self.ready_to_authorize():
            raise GoogleDriveIsNotReadyToAuthorize()
        creds = InstalledAppFlow.from_client_config(
            self._credentials, self._scopes) \
            .run_local_server(port=0)
        self._service = build("drive", "v3", credentials=creds)

    def get_directory_content_list(self, directory):
        if directory == "/":
            return list(filter(lambda file: "parents" not in file,
                               self._get_all_files_list(
                                   ["id", "name", "parents"])))
        raise NotImplementedError()

    def deliver_element(self, element):
        try:
            if self._service is None:
                self.authorize()
            if not isinstance(element, IGoogleDriveBackupable):
                return f"Google drive: не удалось доставить {element.title}," \
                       f"т.к. эта функция для данного элемента не поддерживается"
            return element.backup_to_google_drive(
                self._service, sub_path=self._sub_path)
        except GoogleDriveIsNotReadyToAuthorize:
            return "Не удалось доставить элемент(-ы)," \
                   "т.к. программа не авторизована в google drive"
        except Exception:
            raise
            return "Неизвестная ошибка в Google Drive destination"

    def _get_all_files_list(self, file_fields):
        files = []
        while True:
            response = self._service.files().list(
                pageSize=100,
                fields=f"nextPageToken, files({', '.join(file_fields)})") \
                .execute()
            files += response["files"]
            if "nextPageToken" not in response:
                return files

    # Понадобиться позже
    def _create_files_graph(self, files):
        graph = {}
        for file in files:
            if file["id"] in graph:
                continue
            graph[file["id"]] = Graph(file)
            if "parents" not in file:
                continue
            for parent_id in file["parents"]:
                if parent_id not in graph:
                    graph[parent_id] = Graph(files[parent_id])
                    graph[parent_id].children.append(file)
                    graph[file["id"]].parents.append(files[parent_id])
        return graph

    # TODO
    def _create_directories_list(self, files):
        graph = self._create_files_graph(files)
        directories_list = []
        for root in filter(lambda v: (v.data["mimeType"] ==
                                      "application/vnd.google-apps.folder" and
                                      v.parents == []),
                           graph.values()):
            stack = [root]
            directories_list.append()
            while stack:
                current_folder = stack.pop()
        return None

    @property
    def client_id(self):
        return self._credentials["installed"]["client_id"]

    @property
    def client_secret(self):
        return self._credentials["installed"]["client_secret"]

    @property
    def title(self):
        return self._title

    @property
    def type_description(self):
        return "Google drive облако"

    @property
    def include(self):
        return self._include_flag

    @property
    def sub_path(self):
        return self._sub_path

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

    @title.setter
    @check_type_decorator(str)
    def title(self, value):
        self._title = value

    @sub_path.setter
    @check_type_decorator(str)
    def sub_path(self, value):
        self._sub_path = value

    def _create_credentials(self, client_id, client_secret):
        return {"installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "project_id": "angular-land-288207",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":
                "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
        }}
