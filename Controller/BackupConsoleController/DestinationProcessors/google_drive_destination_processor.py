import re
from Controller.BackupConsoleController.backup_program_processor \
    import BackupProgramProcessor
from Controller.BackupConsoleController.google_drive_processor \
    import GoogleDriveProcessor
from Model.Clouds.google_drive_cloud import GoogleDriveCloud
from enum import Enum


class GDDProcessorState(Enum):
    START = 0
    NAMING = 1
    SETUP_GOOGLE_DRIVE = 2
    SUB_PATH = 3
    COMPLETE = 4


class GoogleDriveDestinationProcessor(BackupProgramProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_destination = GoogleDriveCloud(self._args_provider)
        self._state = GDDProcessorState.START
        self._google_drive_processor = GoogleDriveProcessor(
            self._sender, self._args_provider, self._current_destination)

    def fit_for_request(self, str_request):
        return re.match(r"googleDrive", str_request, re.IGNORECASE)\
               is not None

    def process_request(self, str_request):
        if str_request == "help":
            self._sender.send_text(self.help)
        elif (self._state == GDDProcessorState.START and
              re.match(r"googleDrive", str_request, re.IGNORECASE)
              is not None):
            self._current_task.add_destination(self._current_destination)
            self._sender.send_text(
                "Настройка googleDrive destination\n"
                "Введите название: ", end="")
            self._state = GDDProcessorState.NAMING
        elif self._state == GDDProcessorState.NAMING:
            self._current_destination.title = str_request
            self._sender.send_text("Авторизация в google drive")
            self._google_drive_processor.process_request("start")
            self._state = GDDProcessorState.SETUP_GOOGLE_DRIVE
        elif self._state == GDDProcessorState.SETUP_GOOGLE_DRIVE:
            self._google_drive_processor.process_request(str_request)
            if self._google_drive_processor.is_finished():
                self._state = GDDProcessorState.SUB_PATH
                self._sender.send_text(
                    "Введите sub paths"
                    "(для завершения введите пустую строку): ")
        elif self._state == GDDProcessorState.SUB_PATH:
            if str_request == "":
                self._sender.send_text(
                    "Настройка GoogleDriveDestination завершена")
                self._state = GDDProcessorState.COMPLETE
                return True
            self._current_destination.add_sub_path(str_request)
        elif self._state == GDDProcessorState.COMPLETE:
            self._google_drive_processor.process_request(str_request)
        else:
            self._sender.send_text("Ошибка")

    def is_finished(self):
        return self._state == GDDProcessorState.COMPLETE

    @property
    def help(self):
        pass
