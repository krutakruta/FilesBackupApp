import re
from enum import Enum
from Controller.BackupConsoleController.\
    backup_program_processor import ProgramProcessor
from Controller.BackupConsoleController.\
    yandex_disk_processor import YandexDiskProcessor
from Model.Clouds.yandex_disk_cloud import YandexDiskCloud


class YDSProcessorState(Enum):
    START = 0
    NAMING = 1
    SETUP_YANDEX_DISK = 2
    SOURCE_SUB_PATH = 3
    DESTINATION_SUB_PATH = 4
    COMPLETE = 5


class YandexDiskSourceProcessor(ProgramProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_source = YandexDiskCloud(self._args_provider)
        self._state = YDSProcessorState.START
        self._yandex_disk_processor = YandexDiskProcessor(
            self._sender, self._args_provider, self._current_source)

    def fit_for_request(self, str_request):
        return re.match(r"yandexDisk", str_request, re.IGNORECASE) is not None

    def process_request(self, str_request):
        if str_request == "help":
            self._sender.send_text(self.help)
        elif str_request == "abort":
            self._current_task.remove_source(
                self._current_source.source_title)
            self._state = YDSProcessorState.START
            return True
        elif (self._state == YDSProcessorState.START and
                re.match(r"yandexDisk", str_request, re.IGNORECASE)
                is not None):
            self._current_task.add_destination(self._current_source)
            self._sender.send_text(
                "Настройка yandexDisk destination\n"
                "Введите название: ", end="")
            self._state = YDSProcessorState.NAMING
        elif self._state == YDSProcessorState.NAMING:
            self._current_source.destination_title = str_request
            self._sender.send_text("Авторизация в yandex disk")
            self._yandex_disk_processor.process_request("start")
            self._state = YDSProcessorState.SETUP_YANDEX_DISK
        elif self._state == YDSProcessorState.SETUP_YANDEX_DISK:
            self._yandex_disk_processor.process_request(str_request)
            if self._yandex_disk_processor.is_finished():
                self._sender.send_text(
                    "Введите подпути к файлам из источника"
                    "(для завершения введите пустую строку): ")
                self._state = YDSProcessorState.SOURCE_SUB_PATH
        elif self._state == YDSProcessorState.SOURCE_SUB_PATH:
            if str_request == "":
                self._sender.send_text(
                    "Введите подпуть для сохранения: ")
                self._state = YDSProcessorState.DESTINATION_SUB_PATH
            self._current_source.add_source_sub_path_to_restore(str_request)
        elif self._state == YDSProcessorState.DESTINATION_SUB_PATH:
            self._current_source.add_destination_sub_path_to_restore(str_request)
            self._sender.send_text(
                "Настройка GoogleDriveDestination завершена")
            self._state = YDSProcessorState.COMPLETE
        elif self._state == YDSProcessorState.COMPLETE:
            return self._yandex_disk_processor.process_request(str_request)
        else:
            self._sender.send_text("Ошибка")
        return False

    def is_finished(self):
        return self._state == YDSProcessorState.COMPLETE

    @property
    def help(self):
        return "yandex_disk_source_processor"
