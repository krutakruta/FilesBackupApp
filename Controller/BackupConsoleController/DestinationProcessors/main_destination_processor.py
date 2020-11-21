from enum import Enum
from re import match as re_match
from Controller.BackupConsoleController. \
    backup_program_processor import ProgramProcessor
from Model.model_exceptions import TaskError
from Utilities.useful_functions import \
    process_req_and_remove_sub_proc_if_its_finished


class DestinationProcessorState(Enum):
    START = 0
    SETUP_DESTINATION = 1


class MainDestinationProcessor(ProgramProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_destination = None
        self._state = DestinationProcessorState.START
        self._current_processor = None

    def fit_for_request(self, str_request):
        return re_match(r"add destination.*|remove destination.*",
                        str_request) is not None

    def process_request(self, str_request):
        if str_request == "back":
            if (self._current_destination is None or
                    self._current_destination and
                    self._current_destination.is_finished()):
                self._current_processor = None
                self._current_destination = None
                return True
            else:
                self._sender.send_text(
                    "Не удалось выйти, т.к. настройка не завершена")
        elif str_request == "help" and self._current_processor is None:
            self._sender.send_text(self.help)
        elif self._state == DestinationProcessorState.START:
            self._process_start_state(str_request)
        elif self._state == DestinationProcessorState.SETUP_DESTINATION:
            finished = self._process_adding_destination_state(str_request)
            if finished:
                self._state = DestinationProcessorState.START
            return finished
        return False

    def _process_start_state(self, str_request):
        if re_match(r"add destination.*", str_request) is not None:
            title_match_res = re_match(r"add destination (.+)", str_request)
            if title_match_res is None:
                self._sender.send_text("Вы не ввели название")
            else:
                self._state = DestinationProcessorState.SETUP_DESTINATION
                return self._process_adding_destination_state(
                    title_match_res.group(1))
        elif re_match(r"remove destination.*", str_request) is not None:
            title_match_res = re_match("remove destination (.+)", str_request)
            if title_match_res is None:
                self._sender.send_text("Вы не ввели название")
            else:
                self._remove_destination(str_request)
        else:
            self._send_i_dont_understand()
        return False

    def _process_adding_destination_state(self, str_request):
        if self._current_processor:
            return process_req_and_remove_sub_proc_if_its_finished(
                str_request, self._current_processor,
                self._remove_current_processor)
        for processor in self._args_provider.get_destination_processors(
                current_task=self._current_task,
                sender=self._sender,
                args_provider=self._args_provider):
            if processor.fit_for_request(str_request):
                self._current_processor = processor
                return process_req_and_remove_sub_proc_if_its_finished(
                    str_request, processor, self._remove_current_processor)
        else:
            self._sender.send_text(f"Назначение {str_request} не найдено")

    def _remove_destination(self, str_request):
        title_match_res = re_match(r"remove destination (.*)", str_request)
        if title_match_res is None:
            self._sender.send_text("Вы не указали название")
            return
        try:
            self._current_task.remove_destination(title_match_res.group(1))
            self._sender.send_text(f"Назначение {title_match_res.group(1)} "
                                   f"успешно удалено")
        except TaskError as ex:
            if ex.message is None:
                self._sender.send_text(f"Ошибка при удалении назначени "
                                       f"{title_match_res.group(1)}")
            else:
                self._sender.send_text(f"Ошибка: {ex.message}")

    def _remove_current_processor(self):
        self._current_processor = None

    def _send_i_dont_understand(self):
        self._sender.send_text("Не понял запрос. Справка: help")

    def is_finished(self):
        return False

    @property
    def help(self):
        return "main_destination_processor"
