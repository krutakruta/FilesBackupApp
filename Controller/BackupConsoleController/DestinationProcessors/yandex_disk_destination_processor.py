import re
import webbrowser

import yadisk

from Controller.BackupConsoleController.backup_program_processor import BackupProgramProcessor
from enum import Enum
from Model.BackupDestination\
    .yandex_disk_destination import YandexDiskDestination
from Model.model_exceptions import NotReadyToAuthorizeError,\
    BadConfirmationCodeError, YandexDiskError


class YDDProcessorState(Enum):
    ERROR = 0
    JUST_CREATED = 1
    NAMING = 2
    SUB_PATH = 3
    CLIENT_ID = 4
    CLIENT_SECRET = 5
    CONFIRMATION_CODE = 6
    AUTHORIZED = 7


class YandexDiskDestinationProcessor(BackupProgramProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_destination = None
        self._state = YDDProcessorState.JUST_CREATED

    def fit_for_request(self, str_request):
        return re.match(r"add destination yandexdisk|"
                        r"remove destination yandexdisk.*",
                        str_request, re.IGNORECASE) is not None

    def process_request(self, str_request):
        if str_request == "back":
            self._check_current_destination()
            return True
        elif str_request == "help":
            self._sender.send_text(self.help)
        elif self._state == YDDProcessorState.JUST_CREATED:
            self._handle_just_created_state(str_request)
        elif self._state == YDDProcessorState.NAMING:
            self._handle_naming_state(str_request)
        elif self._state == YDDProcessorState.SUB_PATH:
            self._handle_sub_path_state(str_request)
        elif self._state == YDDProcessorState.CLIENT_ID:
            self._handle_client_id_state(str_request)
        elif self._state == YDDProcessorState.CLIENT_SECRET:
            self._handle_client_secret_state(str_request)
        elif self._state == YDDProcessorState.CONFIRMATION_CODE:
            self._handle_confirmation_code_state(str_request)
        elif self._state == YDDProcessorState.AUTHORIZED:
            self._handle_authorized_state(str_request)
        elif self._state == YDDProcessorState.ERROR:
            self._sender.send_text("Внутренная ошибка")
            return True
        return False

    def _handle_just_created_state(self, str_request):
        command = re.match(r"(.+) destination yandexdisk.*", str_request,
                           re.IGNORECASE).group(1)
        if command == "remove":
            self._remove_destination(str_request)
            return True
        else:
            self._current_destination = YandexDiskDestination(
                self._args_provider)
            self._current_backup_task.add_destination(
                self._current_destination)
            self._sender.send_text("Введите название: ", end="")
            self._state = YDDProcessorState.NAMING

    def _handle_naming_state(self, str_request):
        title = re.match(r"(.*)", str_request).group(1)
        self._current_destination.title = title
        self._sender.send_text("Введите подпуть на yandex disk: ", end="")
        self._state = YDDProcessorState.SUB_PATH

    def _handle_sub_path_state(self, str_request):
        sub_path = re.match(r"(.*)", str_request).group(1)
        self._current_destination.sub_path = sub_path
        self._sender.send_text("Введите client_id: ", end="")
        self._state = YDDProcessorState.CLIENT_ID

    def _handle_client_id_state(self, str_request):
        self._current_destination.client_id = re.match(
            r"(.*)", str_request).group(1)
        self._sender.send_text("Введите client_secret: ", end="")
        self._state = YDDProcessorState.CLIENT_SECRET

    def _handle_client_secret_state(self, str_request):
        self._current_destination.client_secret = re.match(
            r"(.*)", str_request).group(1)
        webbrowser.open(self._current_destination.get_code_url(),
                        new=1, autoraise=True)
        self._sender.send_text(
            f"Разрешите доступ и введите код подтверждения: ", end="")
        self._state = YDDProcessorState.CONFIRMATION_CODE

    def _handle_confirmation_code_state(self, str_request):
        code = re.match(r"(.*)", str_request).group(1)
        try:
            self._current_destination.authorize(code)
            self._sender.send_text("Вы авторизованы")
            self._state = YDDProcessorState.AUTHORIZED
        except NotReadyToAuthorizeError:
            self._sender.send_text("Не заданы client_id или client_secret")
            self._state = YDDProcessorState.ERROR
        except BadConfirmationCodeError:
            self._sender.send_text("Неверный код подтверждения")
        except YandexDiskError:
            self._sender.send_text("Yandex Disk: неизвестная ошибка")
            raise
            self._state = YDDProcessorState.ERROR

    def _handle_authorized_state(self, str_request):
        if re.match(r"set sub_path.*", str_request, re.IGNORECASE):
            match = re.match(r"set sub_path (.+)", str_request, re.IGNORECASE)
            if match is not None:
                self._current_destination.sub_path = match.group(1)
            else:
                self._sender.send_text("Вы не ввели подпуть")
        elif re.match(r"dirlist.*", str_request) is not None:
            path = re.match(r"dirlist ?(.*)", str_request).group(1)
            try:
                self._send_dirlist("/" if path is None or path == ""
                                   else path)
            except yadisk.exceptions.PathNotFoundError:
                self._sender.send_text("Такого подпути не существует")
        else:
            self._send_i_dont_understand()

    def _send_dirlist(self, path):
        for item in self._current_destination.dirlist(path):
            self._sender.send_text(f"- {item}")

    def _remove_destination(self, str_request):
        match_res = re.match(r"remove destination yandexdisk (.+)",
                             str_request, re.IGNORECASE)
        if match_res is None:
            self._sender.send_text("Вы не задали название")
        else:
            self._current_backup_task.remove_destination(match_res.group(1))

    def _check_current_destination(self):
        if not self._current_destination.ready_to_authorize():
            self._current_backup_task.remove_destination(
                self._current_destination.title)
            self._current_destination = None
            self._sender.send_text("Yandex Disk 'удален', т.к. не был настроен")

    def _send_i_dont_understand(self):
        self._sender.send_text("Не понял запрос. Справка: help")

    @property
    def help(self):
        return """После авторизации
Список файлов и папок:
    - dirlist path
Установить подпуть в yandex disk:
    - set sub_path path"""
