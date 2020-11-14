import yadisk
from Model.i_backup_destination import IBackupDestination
from Model.BackupElements.i_yandex_disk_backupable import IYandexDiskBackupable
from Model.model_exceptions import YandexDiskError, InvalidAuthCodeError, \
    NotReadyToAuthorizeError
from Utilities.useful_functions import check_type_decorator


class YandexDiskCloud(IBackupDestination):
    def __init__(self, args_provider, title="YandexDisk"):
        self._args_provider = args_provider
        self._title = title
        self._include_flag = True
        self._sub_paths = ["/"]
        self._service = yadisk.YaDisk()

    def authorize(self, confirmation_code):
        if not self.is_ready_to_authorize():
            raise NotReadyToAuthorizeError()
        try:
            token = self._service.get_token(confirmation_code)["access_token"]
        except yadisk.exceptions.BadRequestError:
            raise InvalidAuthCodeError()
        except Exception:
            raise YandexDiskError()
        if not self._service.check_token(token):
            raise YandexDiskError()
        self._service.token = token

    def is_ready_to_authorize(self):
        return self._service.id and self._service.secret

    def get_code_url(self):
        return self._service.get_code_url()

    def dirlist(self, path):
        return [item.name for item in self._service.listdir(
            path, fields=["name"])]

    def deliver_element(self, element):
        try:
            if self._service is None:
                return "Yandex Disk: не авторизован"
            if not isinstance(element, IYandexDiskBackupable):
                return f"Yandex disk: не удалось доставить {element.title}," \
                       f"т.к. эта функция для данного элемента не поддерживается"
            backup_result = []
            for sub_path in self._sub_paths:
                backup_result.append(element.backup_to_yandex_disk(
                    self._service, sub_path))
            return "\n".join(backup_result)
        except Exception:
            return "Неизвестная ошибка в Yandex Disk destination"

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return "Yandex Disk облако"

    @property
    def include(self):
        return self._include_flag

    @check_type_decorator(str)
    def add_sub_path(self, sub_path):
        self._sub_paths.append(sub_path)

    def remove_sub_path(self, sub_path):
        self._sub_paths.remove(sub_path)

    @property
    def client_id(self):
        return self._service.id

    @property
    def client_secret(self):
        return self._service.secret

    @include.setter
    @check_type_decorator(bool)
    def include(self, value):
        self._include_flag = value

    @client_id.setter
    @check_type_decorator(str)
    def client_id(self, value):
        self._service.id = value

    @client_secret.setter
    @check_type_decorator(str)
    def client_secret(self, value):
        self._service.secret = value

    @title.setter
    @check_type_decorator(str)
    def title(self, value):
        self._title = value
