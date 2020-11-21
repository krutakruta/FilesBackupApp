import re
from enum import Enum
from Controller.BackupConsoleController.backup_program_processor import\
    ProgramProcessor
from Controller.BackupConsoleController.yandex_disk_processor import YandexDiskProcessor
from Model.Clouds.yandex_disk_cloud import YandexDiskCloud


class YDDProcessorState(Enum):
    START = 0
    NAMING = 1
    SETUP_YANDEX_DISK = 2
    SUB_PATH = 3
    COMPLETE = 4


class YandexDiskDestinationProcessor(ProgramProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_destination = YandexDiskCloud(self._args_provider)
        self._state = YDDProcessorState.START
        self._yandex_disk_processor = YandexDiskProcessor(
            self._sender, self._args_provider, self._current_destination)

    def fit_for_request(self, str_request):
        return re.match(r"yandexDisk", str_request, re.IGNORECASE) is not None

    def process_request(self, str_request):
        if (str_request == "help" and
                self._state != YDDProcessorState.COMPLETE):
            self._sender.send_text(self.help)
        elif str_request == "abort":
            self._current_task.remove_destination(
                self._current_destination.destination_title)
            self._state = YDDProcessorState.START
            self._sender.send_text(
                "Настройка yandex disk destination прервана")
            return True
        elif (self._state == YDDProcessorState.START and
                re.match(r"yandexDisk", str_request, re.IGNORECASE)
                is not None):
            self._current_task.add_destination(self._current_destination)
            self._sender.send_text(
                "Настройка yandexDisk source\n"
                "Введите название: ", end="")
            self._state = YDDProcessorState.NAMING
        elif self._state == YDDProcessorState.NAMING:
            self._current_destination.destination_title = str_request
            self._sender.send_text("Авторизация в yandex disk")
            self._yandex_disk_processor.process_request("start")
            self._state = YDDProcessorState.SETUP_YANDEX_DISK
        elif self._state == YDDProcessorState.SETUP_YANDEX_DISK:
            self._yandex_disk_processor.process_request(str_request)
            if self._yandex_disk_processor.is_finished():
                self._sender.send_text(
                    "Введите подпути для сохранения"
                    "(для завершения введите пустую строку): ")
                self._state = YDDProcessorState.SUB_PATH
        elif self._state == YDDProcessorState.SUB_PATH:
            if str_request == "":
                self._sender.send_text(
                    "Настройка GoogleDriveDestination завершена")
                self._state = YDDProcessorState.COMPLETE
            self._current_destination.add_sub_path_to_backup(str_request)
        elif self._state == YDDProcessorState.COMPLETE:
            return self._yandex_disk_processor.process_request(str_request)
        else:
            self._sender.send_text("Ошибка")
        return False

    def is_finished(self):
        return self._state == YDDProcessorState.COMPLETE

    @property
    def help(self):
        return "yandex_disk_destination_processor"
