from Controller.BackupConsoleController.processor import Processor
from enum import Enum
from re import match
from Model.model_exceptions import TaskWithTheSameNameAlreadyExist,\
    ThereIsNoTaskWithSuchName


class CreatingTaskState(Enum):
    START = 0
    SETTING_UP_TASK = 1


class MainProcessor(Processor):
    def __init__(self, sender, backup_program_model, args_provider):
        self._sender = sender
        self._backup_program_model = backup_program_model
        self._state = CreatingTaskState.START
        self._current_task_to_setup = None
        self._current_setting_up_processor = None
        self._args_provider = args_provider

    def fit_for_request(self, str_request):
        return True

    def process_request(self, str_request):
        if str_request == "exit":
            return True
        elif str_request == "help":
            self._sender.send_text(self.help)
        elif self._state == CreatingTaskState.START:
            self._process_request_start_state(str_request)
        elif self._state == CreatingTaskState.SETTING_UP_TASK:
            self._process_request_setting_up_task_state(str_request)
        return False

    def _process_request_start_state(self, str_request):
        if match(r"create task .+", str_request) is not None:
            task_name = match(r"create task (.+)", str_request).group(1)
            try:
                self._backup_program_model.create_task(task_name)
                self._sender.send_text(f"Бэкап {task_name} создан")
            except TaskWithTheSameNameAlreadyExist:
                self._sender.send_text("Бэкап с таким именем уже существует")

        elif match(r"delete task .+", str_request) is not None:
            task_name = match(r"delete task (.+)").group(1)
            try:
                self._backup_program_model.delete_task(task_name)
                self._sender.send_text(f"Бэкап {task_name} удален")
            except ThereIsNoTaskWithSuchName:
                self._sender.send_text("Бэкапа с таким именем не существует")

        elif match(r"setup task .+", str_request) is not None:
            task_name = match(r"setup task (.+)", str_request).group(1)
            if task_name not in self._backup_program_model.get_tasks_dict():
                self._sender.send_text("Такого бэкапа не существует")
                return False
            self._current_task_to_setup =\
                self._backup_program_model.get_tasks_dict()[task_name]
            self._state = CreatingTaskState.SETTING_UP_TASK

        elif match(r"tasks list", str_request) is not None:
            self._send_tasks_list()
        else:
            self._send_i_dont_understand()
        return False

    def _process_request_setting_up_task_state(self, str_request):
        if str_request == "back":
            if self._current_setting_up_processor is None:
                self._state = CreatingTaskState.START
                return True
            self._sender.send_text(
                "Не удалось выйти, т.к. настройка не завершена")
        if self._current_setting_up_processor is not None:
            self._process_req_and_remove_sub_proc_if_its_finished(
                str_request)
            return False
        for processor in self._args_provider.get_all_setting_up_processors(
                current_backup_task=self._current_task_to_setup,
                sender=self._sender,
                args_provider=self._args_provider):
            if processor.fit_for_request(str_request):
                self._current_setting_up_processor = processor
                self._process_req_and_remove_sub_proc_if_its_finished(
                    str_request)
                return False
        else:
            self._send_i_dont_understand()
        return False

    def _process_req_and_remove_sub_proc_if_its_finished(self, string):
        finished = self._current_setting_up_processor.process_request(string)
        self._current_setting_up_processor = \
            None if finished else self._current_setting_up_processor

    def _send_i_dont_understand(self):
        self._sender.send_text("Не понял запрос. Справка: help")

    def _send_tasks_list(self):
        task_dict = self._backup_program_model.get_tasks_dict()
        if len(task_dict) != 0:
            rows_to_send = []
            counter = 1
            for name in task_dict.keys():
                rows_to_send.append(f"{counter} - {name}")
                counter += 1
            self._sender.send_text("\n".join(rows_to_send))
        else:
            self._sender.send_text("Список пуст")


    @property
    def help(self):
        if self._state == CreatingTaskState.START:
            return """Создание бэкапа:
- create task task_name
Настройка бэкапа:
- setup task task_name
Удаление бэкапа:
- delete task task_name
Список бэкапов:
- tasks list"""
        else:
            return """Доступные команды:
- add/remove file file_name/file_path
- add/remove destination destination_name"""


