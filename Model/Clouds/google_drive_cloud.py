from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from oauthlib.oauth2.rfc6749 import errors as google_drive_errors

from Model.RestoreElements.\
    i_google_drive_recovering import IGoogleDriveRecovering
from Model.RestoreElements.i_restore_element import IRestoreElement
from Model.i_backup_destination import IBackupDestination
from Model.BackupElements \
    .i_google_drive_backupable import IGoogleDriveBackupable
from Model.i_files_source import IFilesSource
from Model.model_exceptions import NotReadyToAuthorizeError, \
    ThereIsNoSubPathLikeThatInGoogleDrive, InvalidClientError,\
    InvalidAuthCodeError
from Utilities.useful_functions import check_type_decorator, split_path
from Utilities.useful_functions import parse_path_and_get_path_sheet


AUTHORIZATION_PROMPT_MESSAGE = "Перейдите по ссылке для авторизации {url}"
DEFAULT_AUTH_CODE_MESSAGE = "Введите полученный код: "
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"


class Graph:
    def __init__(self, data):
        self.data = data
        self.parents = []
        self.children = []


class GoogleDriveCloud(IBackupDestination, IFilesSource):
    def __init__(self, args_provider, dest_title="Google Drive destination",
                 source_title="Google Drive source",
                 client_id=None, client_sec=None):
        self._destination_title = dest_title
        self._source_title = source_title
        self._sub_paths_to_backup = []
        self._destination_sub_path_to_restore = "/"
        self._credentials = self._create_credentials(client_id, client_sec)
        self._scopes = ['https://www.googleapis.com/auth/drive']
        self._service = None
        self._args_provider = args_provider

    def is_ready_to_authorize(self):
        return (self._credentials["installed"]["client_id"] and
                self._credentials["installed"]["client_secret"])

    def authorize(
            self, authorization_prompt_message=AUTHORIZATION_PROMPT_MESSAGE,
            authorization_code_message=DEFAULT_AUTH_CODE_MESSAGE):
        try:
            if not self.is_ready_to_authorize():
                raise NotReadyToAuthorizeError()
            creds = InstalledAppFlow.from_client_config(
                self._credentials, self._scopes, redirect_uri=REDIRECT_URI) \
                .run_console(authorization_prompt_message,
                             authorization_code_message)
            self._service = build("drive", "v3", credentials=creds)
        except google_drive_errors.InvalidGrantError:
            raise InvalidAuthCodeError()
        except google_drive_errors.InvalidClientError:
            raise InvalidClientError()

    def is_ready(self):
        return self._service is not None

    @check_type_decorator(Resource)
    def set_google_service(self, service):
        self._service = service

    def get_directory_content_dict_id_files(self, path):
        try:
            if path == "/":
                return {"корневой каталог":
                            list(filter(lambda file: "parents" not in file,
                                        GoogleDriveCloud._get_all_files_list(
                                            self._service,
                                            ["id", "name", "parents"])))}
            target_folders = GoogleDriveCloud. \
                get_target_folders_of_not_root_path_in_google_drive(
                    self._service, path)
            files = {}
            for folder in target_folders:
                files[folder["id"]] = []
                response = self._service.files().list(
                    q=f"'{folder['id']}' in parents", fields="files(id, name)"
                ).execute()
                if response:
                    files[folder["id"]] += response["files"]
            return files
        except ThereIsNoSubPathLikeThatInGoogleDrive:
            return {}

    def get_all_directories(self):
        files = self._service.files().list(
            q=f"mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name, parents)"
        ).execute()
        if files is None:
            return []
        folders = files["files"]
        directories = []
        for folder in filter(lambda f: "parents" not in f, folders):
            self._restore_directories(folder, folders, [], directories)
        return list(map(lambda d:
                        f"/{'/'.join(map(lambda item: item['name'], d))}/",
                        directories))

    def _restore_directories(self, curr_folder, folders,
                             current_directory_elements, directories):
        current_directory_elements.append(curr_folder)
        has_children = False
        for folder in filter(lambda f: "parents" in f and
                                       curr_folder["id"] in f["parents"],
                             folders):
            has_children = True
            self._restore_directories(
                folder, folders, [_ for _ in current_directory_elements], directories)
        if not has_children:
            directories.append(current_directory_elements)

    def deliver_element(self, element):
        try:
            if self._service is None:
                self.authorize()
            if not isinstance(element, IGoogleDriveBackupable):
                return f"GoogleDriveBackup: не удалось доставить " \
                       f"{element.destination_title}," \
                       f"т.к. эта функция для данного элемента " \
                       f"не поддерживается"
            backup_result = []
            for sub_path in self._sub_paths_to_backup:
                backup_result.append(element.backup_to_google_drive(
                    self._service, dst_path=sub_path))
            return "\n".join(backup_result)
        except NotReadyToAuthorizeError:
            return "GoogleDriveBackup: Не удалось доставить элемент(-ы)," \
                   "т.к. программа не авторизована в google drive"
        except Exception:
            return "Неизвестная ошибка в Google Drive destination"

    def restore(self, element):
        try:
            if self._service is None:
                self.authorize()
            if not isinstance(element, IGoogleDriveRecovering):
                return f"GoogleDriveRestore: не удалось доставить " \
                       f"{element.source_title}," \
                       f"т.к. эта функция для данного элемента " \
                       f"не поддерживается"
            return element.restore_from_google_drive(
                self._service, self._destination_sub_path_to_restore)
        except NotReadyToAuthorizeError:
            return "GoogleDriveRestore: не удалось восстановить элемент, " \
                   "т.к. программа не авторизована в Google Drive"
        except Exception:
            return "Неизвестная ошибка в Google Drive Source"

    @staticmethod
    def get_target_folders_of_not_root_path_in_google_drive(service, path):
        path_items = split_path(path)
        if not path_items:
            raise ValueError()
        files = service.files().list(
            q=f"mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name, parents)"
        ).execute()
        if not files or path_items == []:
            return []
        folders = files["files"]
        target_folders = []
        for folder in filter(lambda f: f["name"] == path_items[0], folders):
            GoogleDriveCloud._find_target_folders(
                folders, folder, 1, path_items, target_folders)
        if not target_folders:
            raise ThereIsNoSubPathLikeThatInGoogleDrive()
        return target_folders

    @staticmethod
    def get_target_files(service, path):
        path_items = split_path(path)
        if len(path_items) == 1:
            return service.files().list(
                q=f"name={path_items[-1]}",
                field="files(id, name)").execute()["files"]
        target_folders = GoogleDriveCloud.\
            get_target_folders_of_not_root_path_in_google_drive(
                "/".join(path_items[:-1]))
        files = []
        for folder in target_folders:
            files += service.files().list(
                    q=f"{folder['id']} in parents and name={path_items[-1]}",
                    fields="files(id, name)").execute()["files"]
        return files

    @staticmethod
    def _find_target_folders(folders, curr_folder,
                             depth, path_items, target_folders):
        if depth == len(path_items):
            target_folders.append(curr_folder)
            return
        for fol in filter(lambda f: (f["name"] == path_items[depth] and
                                     curr_folder["id"] in f["parents"]),
                          folders):
            GoogleDriveCloud._find_target_folders(
                folders, fol, depth + 1, path_items, target_folders)

    @staticmethod
    def _get_all_files_list(google_service, file_fields):
        files = []
        while True:
            response = google_service.files().list(
                pageSize=100,
                fields=f"nextPageToken, files({', '.join(file_fields)})") \
                .execute()
            files += response["files"]
            if "nextPageToken" not in response:
                return files

    # Понадобится позже
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
        raise NotImplementedError()
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
    def source_title(self):
        return self._source_title

    @property
    def source_description(self):
        return "Google drive облако"

    @check_type_decorator(str)
    def set_destination_sub_path_to_restore(self, sub_path):
        self._destination_sub_path_to_restore = sub_path

    @property
    def destination_title(self):
        return self._destination_title

    @property
    def destination_description(self):
        return "Google drive облако"

    def add_sub_path_to_backup(self, sub_path):
        self._sub_paths_to_backup.append(sub_path)

    def remove_backup_sub_path(self, sub_path):
        self._sub_paths_to_backup.remove(sub_path)

    @destination_title.setter
    @check_type_decorator(str)
    def destination_title(self, value):
        self._destination_title = value

    @source_title.setter
    @check_type_decorator(str)
    def source_title(self, value):
        self._source_title = value

    @client_id.setter
    @check_type_decorator(str)
    def client_id(self, value):
        self._credentials["installed"]["client_id"] = value

    @client_secret.setter
    @check_type_decorator(str)
    def client_secret(self, value):
        self._credentials["installed"]["client_secret"] = value

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
