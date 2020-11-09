from Controller.BackupConsoleController.processor import Processor
from Model.Clouds \
    .google_drive_cloud import GoogleDriveCloud
from enum import Enum
import re


class GDProcessorState(Enum):
    START = 0
    CLIENT_ID = 1
    CLIENT_SECRET = 2
    AUTHORIZED = 3


class GoogleDriveProcessor(Processor):
    def __init__(self, sender, args_provider, google_drive_model):
        self._sender = sender
        self._args_provider = args_provider
        self._state = GDProcessorState.START
        self._google_drive_model = google_drive_model

    def fit_for_request(self, str_request):
        return True

    def process_request(self, str_request):
        if str_request == "back":
            return True
        elif str_request == "help":
            self._sender.send_text(self.help)
        elif self._state == GDProcessorState.CLIENT_ID:
            self._handle_client_id_state(str_request)
        elif self._state == GDProcessorState.CLIENT_SECRET:
            self._handle_client_secret_state(str_request)
        elif self._state == GDProcessorState.AUTHORIZED:
            return self._handle_authorized_state(str_request)
        elif str_request == "start":
            self._sender.send_text("Введите client_id: ", end="")
            self._state = GDProcessorState.CLIENT_ID
        return False

    def _handle_client_id_state(self, str_request):
        self._google_drive_model.client_id = re.match(
            r"(.+)", str_request).group(1)
        self._sender.send_text("Введите client_secret: ", end="")
        self._state = GDProcessorState.CLIENT_SECRET

    def _handle_client_secret_state(self, str_request):
        self._google_drive_model.client_secret = re.match(
            r"(.+)", str_request).group(1)
        self._google_drive_model.authorize()
        self._sender.send_text("Вы авторизованы. Google drive добавлен")
        self._state = GDProcessorState.AUTHORIZED

    def _handle_authorized_state(self, str_request):
        if re.match(r"directories", str_request) is not None:
            self._sender.send_text(
                "\n".join(self._google_drive_model.get_all_directories()))
        elif re.match(r"dirlist .+", str_request) is not None:
            content_dict = self._google_drive_model.\
                get_directory_content_dict_id_files(
                    re.match(r"dirlist (.+)", str_request).group(1))
            if not content_dict:
                self._sender.send_text("Такого подпути не существует")
            else:
                self._sender.send_text("По вашему запросу найдено следующее:")
                for folder_id in content_dict.keys():
                    self._sender.send_text(f"Папка с id {folder_id}")
                    for item in content_dict[folder_id]:
                        self._sender.send_text(f"- {item['name']}")
        else:
            self._sender.send_text("Неправильный запрос. Справка: help")

    def is_finished(self):
        return self._state == GDProcessorState.AUTHORIZED

    @property
    def help(self):
        return """
Для авторизации в Google Drive необходимы следующие параметры:
- client_id
- client_secret,
которые предоставляются при подключеннии google drive api

После авторизации:
    Псевдограф каталогов:
        - directories
    Список файлов и каталогов по указанному пути('/' - корень):
        - dirlist path"""

