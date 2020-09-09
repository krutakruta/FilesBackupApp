from Controller.BackupConsoleController.MessageProcessors.processor import Processor
import re


class DestinationProcessor(Processor):
    def __init__(self, current_backup_task, sender):
        self._current_backup_task = current_backup_task
        self._sender = sender

    def fit_for_request(self, str_request):
        return re.match(r"add destination.*|remove destination.*", str_request,
                        re.IGNORECASE) is not None

    def process_request(self, str_request):
        match_result = re.match(r"(\w+) destination (.*)")
        command = match_result.group(1)
        if command == "remove":


    @property
    def help(self):
        pass