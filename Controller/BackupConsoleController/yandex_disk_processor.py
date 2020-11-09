import re
import webbrowser

import yadisk

from Controller.BackupConsoleController.processor import Processor
from enum import Enum
from Model.Clouds\
    .yandex_disk_cloud import YandexDiskCloud
from Model.model_exceptions import NotReadyToAuthorizeError,\
    BadConfirmationCodeError, YandexDiskError


class YDProcessorState(Enum):
    ERROR = 0
    CLIENT_ID = 1
    CLIENT_SECRET = 2
    CONFIRMATION_CODE = 3
    AUTHORIZED = 4


class YandexDiskDestinationProcessor(Processor):
    def __init__(self, sender, args_provider):
        self._sender = sender
        self._args_provider = args_provider
        self._yandex_disk_model = YandexDiskCloud(args_provider)
        self._state = YDProcessorState.CLIENT_ID

    def fit_for_request(self, str_request):
        return re.match(r"yandexdisk", str_request, re.IGNORECASE) is not None

    def process_request(self, str_request):
        if str_request == "back":
            return True
        elif str_request == "help":
            self._sender.send_text(self.help)
        elif self._state == YDProcessorState.CLIENT_ID:
            self._handle_client_id_state(str_request)
        elif self._state == YDProcessorState.CLIENT_SECRET:
            self._handle_client_secret_state(str_request)
        elif self._state == YDProcessorState.CONFIRMATION_CODE:
            self._handle_confirmation_code_state(str_request)
        elif self._state == YDProcessorState.AUTHORIZED:
            self._handle_authorized_state(str_request)
        elif self._state == YDProcessorState.ERROR:
            self._sender.send_text("Внутренная ошибка")
            return True
        return False

    def _handle_client_id_state(self, str_request):
        self._yandex_disk_model.client_id = re.match(
            r"(.*)", str_request).group(1)
        self._sender.send_text("Введите client_secret: ", end="")
        self._state = YDProcessorState.CLIENT_SECRET

    def _handle_client_secret_state(self, str_request):
        self._yandex_disk_model.client_secret = re.match(
            r"(.*)", str_request).group(1)
        webbrowser.open(self._yandex_disk_model.get_code_url(),
                        new=1, autoraise=True)
        self._sender.send_text(
            f"Разрешите доступ и введите код подтверждения: ", end="")
        self._state = YDProcessorState.CONFIRMATION_CODE

    def _handle_confirmation_code_state(self, str_request):
        code = re.match(r"(.*)", str_request).group(1)
        try:
            self._yandex_disk_model.authorize(code)
            self._sender.send_text("Вы авторизованы")
            self._state = YDProcessorState.AUTHORIZED
        except NotReadyToAuthorizeError:
            self._sender.send_text("Не заданы client_id или client_secret")
            self._state = YDProcessorState.ERROR
        except BadConfirmationCodeError:
            self._sender.send_text("Неверный код подтверждения")
        except YandexDiskError:
            self._sender.send_text("Yandex Disk: неизвестная ошибка")
            raise
            self._state = YDProcessorState.ERROR

    def _handle_authorized_state(self, str_request):
        if re.match(r"dirlist.*", str_request) is not None:
            path = re.match(r"dirlist ?(.*)", str_request).group(1)
            try:
                self._send_dirlist("/" if path is None or path == ""
                                   else path)
            except yadisk.exceptions.PathNotFoundError:
                self._sender.send_text("Такого подпути не существует")
        else:
            self._send_i_dont_understand()

    def _send_dirlist(self, path):
        for item in self._yandex_disk_model.dirlist(path):
            self._sender.send_text(f"- {item}")

    def _send_i_dont_understand(self):
        self._sender.send_text("Не понял запрос. Справка: help")

    def is_finished(self):
        return self._state == YDProcessorState.AUTHORIZED

    @property
    def help(self):
        return """После авторизации
Список файлов и папок:
    - dirlist path
Установить подпуть в yandex disk:
    - set sub_path path"""
