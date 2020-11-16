from re import match as re_match
from Controller.BackupConsoleController.backup_program_processor import \
    BackupProgramProcessor
from enum import Enum


class FilesRestoreProcessorState(Enum):
    START = 0
    SOURCE = 1


class FilesRestoreProcessor(BackupProgramProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = FilesRestoreProcessorState.START

    def fit_for_request(self, str_request):
        return re_match(r"restore files.*", str_request) is not None

    def process_request(self, str_request):
        if str_request == "back":
            return True
        elif str_request == "help":
            self._sender.send_text(self.help)
        elif self._state == FilesRestoreProcessorState.START:
            return self._handle_start_state(str_request)
        elif self._state == FilesRestoreProcessorState.SOURCE:
            pass

    def _handle_start_state(self, str_request):
        if re_match(r"restore files.*", str_request) is not None:
            self._sender.send_text("Введите источник файлов: ")
            self._state = FilesRestoreProcessorState.SOURCE
        else:
            self._send_i_dont_understand()

    def _send_i_dont_understand(self):
        self._sender.send_text("Не понл запрос. Справка: help")

    def is_finished(self):
        return True

    @property
    def help(self):
        pass

