import re
from Controller.BackupConsoleController.backup_program_processor import BackupProgramProcessor
from enum import Enum

from Model.BackupDestination.yandex_disk_destination import YandexDiskDestination


class YDDProcessorState(Enum):
    JUST_CREATED = 0
    NAMING = 1
    SUB_PATH = 2
    CLIENT_ID = 3
    CONFIRMATION_CODE = 4
    AUTHORIZED = 5


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
                self._sender.send_text("Введите client_id: ", end="")
                self._state = YDDProcessorState.CLIENT_ID
        elif self._state == YDDProcessorState.CLIENT_ID:
            pass

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

    @property
    def help(self):
        pass