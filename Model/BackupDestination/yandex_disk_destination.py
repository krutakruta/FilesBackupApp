import yadisk
from Model.BackupDestination.i_backup_destination import IBackupDestination
from Model.model_exceptions import YandexDiskError, BadConfirmationCodeError, \
    BadTokenError, NotReadyToAuthorizeError
from Utilities.useful_functions import check_type_decorator


class YandexDiskDestination(IBackupDestination):
    def __init__(self, args_provider, title="YandexDisk"):
        self._args_provider = args_provider
        self._title = title
        self._include_flag = True
        self.sub_path = "/"
        self._service = yadisk.YaDisk()

    def authorize(self, confirmation_code):
        if not self.is_ready_to_authorize():
            raise NotReadyToAuthorizeError()
        try:
            token = self._service.get_token(confirmation_code)\
                .pop("access_token", None)
        except yadisk.exceptions.BadRequestError:
            raise BadConfirmationCodeError()
        except Exception:
            raise YandexDiskError()
        if not self._service.check_token(token):
            raise YandexDiskError()
        self._service.token = token

    def is_ready_to_authorize(self):
        return self._service.id and self._service.secret

    def get_code_url(self):
        return self._service.get_code_url()

    def deliver_element(self, element):


    @property
    def title(self):
        return self._title

    @property
    def type_description(self):
        return "Yandex Disk облако"

    @property
    def include(self):
        return self._include_flag

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
        self._service.client_id = value

    @client_secret.setter
    @check_type_decorator(str)
    def client_secret(self, value):
        self._service.secret = value

    @title.setter
    @check_type_decorator(str)
    def title(self, value):
        self._title = value
