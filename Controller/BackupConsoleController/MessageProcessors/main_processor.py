from Controller.BackupConsoleController.MessageProcessors\
    .processor import Processor
from enum import Enum
from re import match
from Model.model_exceptions import TaskWithTheSameNameAlreadyExist


class CreatingTaskState(Enum):
    START = 0
    SETTING_UP_TASK = 1


class MainProcessor(Processor):
    def __init__(self, sender, backup_program_model):
        self._sender = sender
        self._backup_program_model = backup_program_model
        self._state = CreatingTaskState.START
        self._current_task_to_setup = None

    def fit_for_request(self, str_request):
        return True

    def process_request(self, str_request):
        if self._state == CreatingTaskState.START:
            return self._process_request_start_state(str_request)
        if self._state == CreatingTaskState.SETTING_UP_TASK:
            self._process_request_setting_up_state(str_request)

    def _process_request_start_state(self, str_request):
        if match(r"create task \.+", str_request) is not None:
            match_result = match(r"create task \.+", str_request)
            try:
                self._backup_program_model.create_task(match_result.group(1))
            except TaskWithTheSameNameAlreadyExist:
                self._sender.send_text("Бэкап с таким именем уже существует")
        elif match(r"setup task \.+", str_request) is not None:
            self._state = CreatingTaskState.SETTING_UP_TASK
            task_name = match(r"setup task (\.+)", str_request).group(1)
            if task_name not in self._backup_program_model.get_tasks_dict():
                self._sender.send_text("Такого бэкапа не существует")
                return False
            self._current_task_to_setup =\
                self._backup_program_model.get_tasks_dict()[task_name]
        elif str_request == "help":
            self._sender.send_text(self.help)
        else:
            self._sender.send_text("Не понял запрос. Справка: help")
        return False

    def _process_request_setting_up_state(self):
        pass

    @property
    def help(self):
        pass

