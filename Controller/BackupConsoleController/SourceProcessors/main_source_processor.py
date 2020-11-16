import re
from enum import Enum
from Controller.BackupConsoleController.\
    backup_program_processor import BackupProgramProcessor
from Utilities.useful_functions import\
    process_req_and_remove_sub_proc_if_its_finished


class SourceProcessorState(Enum):
    START = 0
    SETUP_SOURCE = 1


class MainSourceProcessor(BackupProgramProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_source = None
        self._state = SourceProcessorState.START
        self._current_processor = None

    def fit_for_request(self, str_request):
        return re.match(r"add source.*|remove source.*|"
                        r"setup source.*", str_request) is not None

    def process_request(self, str_request):
        if str_request == "back":
            if (self._current_source is None or
                    self._current_source and
                    self._current_source.is_finished()):
                return True
            else:
                self._sender.send_text(
                    "Не удалось выйти, т.к. настройка не завершена")
        elif str_request == "help":
            self._sender.send_text(self.help)
        elif self._state == SourceProcessorState.START:
            self._process_start_state(str_request)
        elif self._state == SourceProcessorState.SETUP_SOURCE:
            return self._process_adding_source_state(str_request)
        return False

    def _process_start_state(self, str_request):
        if re.match(r"add source.*", str_request) is not None:
            self._state = SourceProcessorState.SETUP_SOURCE
            return self._process_adding_source_state(
                re.match(r"add source(.*)", str_request).group(1).strip())
        elif re.match(r"remove source.*", str_request) is not None:
            self._remove_source(str_request)
        return False

    def _process_adding_source_state(self, str_request):
        if self._current_processor:
            return process_req_and_remove_sub_proc_if_its_finished(
                str_request, self._current_processor,
                self._remove_current_processor)
        for processor in self._args_provider.get_all_source_processors(
                current_task=self._current_task,
                sender=self._sender,
                args_provider=self._args_provider):
            if processor.fit_for_request(str_request):
                self._current_processor = processor
                return process_req_and_remove_sub_proc_if_its_finished(
                    str_request, processor, self._remove_current_processor)
        else:
            self._sender.send_text("Не понял запрос. Справка: help")

    def _remove_current_processor(self):
        self._current_processor = None

    def is_finished(self):
        return True

    @property
    def help(self):
        pass