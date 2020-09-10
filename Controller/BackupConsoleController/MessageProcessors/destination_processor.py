from Controller.BackupConsoleController.MessageProcessors\
    .processor import Processor
from Model.BackupDestination\
    .google_drive_destination import GoogleDriveDestination
from enum import Enum
import re


class DestinationProcessorState(Enum):
    SETTING_UP_CERTAIN_DESTINATION = 0
    START = 1


class DestinationProcessor(Processor):
    def __init__(self, current_backup_task, sender, args_provider):
        self._current_backup_task = current_backup_task
        self._current_destination_processor = None
        self._state = DestinationProcessorState.START
        self._sender = sender
        self._args_provider = args_provider

    def fit_for_request(self, str_request):
        return re.match(r"add destination.*|remove destination.*", str_request,
                        re.IGNORECASE) is not None

    def process_request(self, str_request):
        if self._state == DestinationProcessorState.START:
            return self._process_start_state(str_request)
        return self._process_setting_up_destination_state(str_request)

    def _process_start_state(self, str_request):
        if str_request == "back":
            return True
        match_result = re.match(r"(\w+) destination (.+)")
        command = match_result.group(1)
        if command == "remove":
            self._current_backup_task.remove_destination(
                match_result.group(2))
        elif command == "add":
            return self._process_setting_up_destination_state(
                match_result.group(2))
        return False

    def _process_setting_up_destination_state(self, str_request):
        if not self._current_setting_up_processor:
            return self._process_req_and_remove_sub_proc_if_its_finished(
                str_request)
        for processor in self._args_provider.get_all_destination_processors(
                            current_backup_task=self._current_backup_task,
                            sender=self._sender,
                            args_provider=self._args_provider):
            if processor.fit_for_request(str_request):
                self._current_destination_processor = processor
                return self._process_req_and_remove_sub_proc_if_its_finished(
                    str_request)
        else:
            self._send_i_dont_understand()
        return False

    def _process_req_and_remove_sub_proc_if_its_finished(self, str_request):
        finished = self._current_setting_up_processor.process_request(
            str_request)
        self._current_setting_up_processor = \
            None if finished else self._current_setting_up_processor
        self._state = (DestinationProcessorState.START if finished
                       else self._state)
        return finished

    def _send_i_dont_understand(self):
        self._sender.send_text("Не понял запрос. Справка: help")

    @property
    def help(self):
        return "help doesn't work yet"
