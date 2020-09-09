from Controller.BackupConsoleController.MessageProcessors\
    .processor import Processor
import re


class GoogleDriveDestinationProcessor(Processor):
    def __init__(self, current_backup_task, sender):
        self._current_backup_task = current_backup_task
        self._sender = sender

    def fit_for_request(self, str_request):
        return re.match(r"googleDrive|google drive|google_drive",
                        str_request, re.IGNORECASE) is not None

    def process_request(self, str_request):
        pass

    @property
    def help(self):
        return """"""