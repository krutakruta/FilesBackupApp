from Controller.BackupConsoleController.MessageProcessors.\
    processor import Processor
from re import match


class AddElementProcessor(Processor):
    def __init__(self, adding_element_processors):
        self._adding_element_processors = adding_element_processors
        self._current_adding_processor = None

    def fit_for_request(self, string):
        return match("/w+? /w/W") is not None

    @property
    def help(self):
        return "\n\n".join([p.help for p in self._adding_element_processors])
