import re
from enum import Enum
from Controller.BackupConsoleController.\
    backup_program_processor import ProgramProcessor
from Controller.BackupConsoleController.\
    google_drive_processor import GoogleDriveProcessor
from Model.Clouds.google_drive_cloud import GoogleDriveCloud
from Model.file import File


class GDSProcessorState(Enum):
    START = 0
    NAMING = 1
    SETUP_GOOGLE_DRIVE = 2
    DESTINATION_SUB_PATH = 3
    ADD_FILE_REMAINING = 4
    COMPLETE = 5


class GoogleDriveSourceProcessor(ProgramProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._state = GDSProcessorState.START
        self._current_source = GoogleDriveCloud(self._args_provider)
        self._google_drive_processor = GoogleDriveProcessor(
            self._sender, self._args_provider, self._current_source)

    def fit_for_request(self, str_request):
        return re.match(r"googleDrive", str_request, re.IGNORECASE)\
               is not None

    def process_request(self, str_request):
        if str_request == "help" and self._state != GDSProcessorState.COMPLETE:
            self._sender.send_text(self.help)
        if str_request == "abort":
            self._current_task.remove_source(
                self._current_source.source_title)
            self._state = GDSProcessorState.START
            self._sender.send_text("Настройка google drive source прервана")
            return True
        elif (self._state == GDSProcessorState.START and
              re.match(r"googleDrive", str_request, re.IGNORECASE)
              is not None):
            self._current_task.add_source(self._current_source)
            self._sender.send_text(
                "Настройка googleDrive source\n"
                "Введите название: ", end="")
            self._state = GDSProcessorState.NAMING
        elif self._state == GDSProcessorState.NAMING:
            self._current_source.source_title = str_request
            self._sender.send_text("Авторизация в google drive")
            self._google_drive_processor.process_request("start")
            self._state = GDSProcessorState.SETUP_GOOGLE_DRIVE
        elif self._state == GDSProcessorState.SETUP_GOOGLE_DRIVE:
            self._google_drive_processor.process_request(str_request)
            if self._google_drive_processor.is_finished():
                self._state = GDSProcessorState.DESTINATION_SUB_PATH
                self._sender.send_text(
                    "Введите путь для сохранения: ", end="")
        elif self._state == GDSProcessorState.DESTINATION_SUB_PATH:
            self._current_source.set_destination_sub_path_to_restore(str_request)
            self._sender.send_text(
                "Введите путь к файлам на google drive"
                "(для завершения введите пустую строку): ", end="")
            self._state = GDSProcessorState.ADD_FILE_REMAINING
        elif self._state == GDSProcessorState.ADD_FILE_REMAINING:
            if str_request != "":
                self._current_task.add_element_to_restore(
                    File(file_path=str_request), self._current_source)
            else:
                self._sender.send_text("Настройка Google Drive source завершена")
                self._state = GDSProcessorState.COMPLETE
        elif self._state == GDSProcessorState.COMPLETE:
            return self._google_drive_processor.process_request(str_request)
        else:
            self._sender.send_text("Ошибка")
        return False

    def is_finished(self):
        return self._state == GDSProcessorState.COMPLETE

    @property
    def help(self):
        return "google_drive_source_processor"
