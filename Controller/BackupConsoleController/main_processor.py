from Controller.BackupConsoleController.processor import Processor
from enum import Enum
from re import match
from Model.model_exceptions import TaskWithTheSameNameAlreadyExist, \
    ThereIsNoTaskWithSuchName
from Utilities.useful_functions import \
    process_req_and_remove_sub_proc_if_its_finished


class CreatingTaskState(Enum):
    START = 0
    SETUP_BACKUP_TASK = 1
    SETUP_RESTORE_TASK = 2


class MainProcessor(Processor):
    def __init__(self, sender, backup_program_model, args_provider):
        self._sender = sender
        self._program_model = backup_program_model
        self._state = CreatingTaskState.START

        self._current_backup_task_to_setup = None
        self._current_restore_task_to_setup = None

        self._current_setup_backup_task_processor = None
        self._current_setup_restore_task_processor = None

        self._args_provider = args_provider

    def fit_for_request(self, str_request):
        return True

    def process_request(self, str_request):
        if str_request == "exit":
            return True
        elif self._state == CreatingTaskState.START:
            self._process_request_start_state(str_request)
        elif self._state == CreatingTaskState.SETUP_BACKUP_TASK:
            self._process_request_setup_backup_task_state(str_request)
        elif self._state == CreatingTaskState.SETUP_RESTORE_TASK:
            self._process_request_setup_restore_task_state(str_request)
        return False

    def is_finished(self):
        return False

    def _process_request_start_state(self, str_request):
        if str_request == "help":
            self._sender.send_text(self.help)
        elif match(r"create backup task .+", str_request) is not None:
            self._create_backup_task(
                match(r"create backup task (.+)", str_request).group(1))

        elif match(r"delete backup task .+", str_request) is not None:
            self._delete_backup_task(
                match(r"delete backup task (.+)", str_request).group(1))

        elif match(r"setup backup task .+", str_request) is not None:
            self._setup_backup_task(
                match(r"setup backup task (.+)", str_request).group(1))

        elif match(r"launch backup .+", str_request) is not None:
            task_name = match(r"launch backup (.+)", str_request).group(1)
            if task_name not in self._program_model.get_backup_tasks_dict():
                self._sender.send_text("Такого бэкапа не существует")
                return False
            self._sender.send_text("Бэкап завершен. Результат:\n")
            self._sender.send_text(
                "\n".join(self._program_model.launch_backup(task_name)))

        elif match(r"create restore task .+", str_request) is not None:
            self._create_restore_task(
                match(r"create restore task (.+)", str_request).group(1))

        elif match(r"setup restore task .+", str_request) is not None:
            self._setup_restore_task(
                match(r"setup restore task (.+)", str_request).group(1))

        elif match(r"delete restore task .+", str_request) is not None:
            self._program_model.delete_restore_task(
                match(r"delete restore task (.+)").group(1))

        elif match(r"launch restore .+", str_request) is not None:
            task_name = match(r"launch restore (.+)", str_request).group(1)
            if task_name not in self._program_model.get_restore_tasks_dict():
                self._sender.send_text("Такой задачи не существует")
                return False
            self._sender.send_text("Задача завершена. Результат:\n")
            self._sender.send_text(
                "\n".join(self._program_model.launch_restore()))

        elif match(r"tasks list", str_request) is not None:
            self._send_backup_tasks_list()
            self._send_restore_tasks_list()
        else:
            self._send_i_dont_understand()
        return False

    def _create_backup_task(self, task_name):
        try:
            self._program_model.create_backup_task(task_name)
            self._sender.send_text(f"Бэкап '{task_name}' создан")
        except TaskWithTheSameNameAlreadyExist:
            self._sender.send_text("Бэкап с таким именем уже существует")

    def _create_restore_task(self, task_name):
        try:
            self._program_model.create_restore_task(task_name)
            self._sender.send_text(
                f"Задача восстановления '{task_name}' создана")
        except TaskWithTheSameNameAlreadyExist:
            self._sender.send_text(
                "Задача восстановления с таким именем уже существует")

    def _delete_backup_task(self, task_name):
        try:
            self._program_model.delete_backup_task(task_name)
            self._sender.send_text(f"Бэкап {task_name} удален")
        except ThereIsNoTaskWithSuchName:
            self._sender.send_text("Бэкапа с таким именем не существует")

    def _setup_backup_task(self, task_name):
        if task_name not in self._program_model.get_backup_tasks_dict():
            self._sender.send_text("Такого таска не существует")
            return False
        self._current_backup_task_to_setup = \
            self._program_model.get_backup_tasks_dict()[task_name]
        self._sender.send_text(f"Настройки бэкапа '{task_name}'")
        self._state = CreatingTaskState.SETUP_BACKUP_TASK

    def _setup_restore_task(self, task_name):
        if task_name not in self._program_model.get_restore_tasks_dict():
            self._sender.send_text("Такого таска не существует")
            return False
        self._current_restore_task_to_setup = \
            self._program_model.get_restore_tasks_dict()[task_name]
        self._sender.send_text(f"Настройка задачи восстановления '{task_name}'")
        self._state = CreatingTaskState.SETUP_RESTORE_TASK

    def _process_request_setup_backup_task_state(self, str_request):
        finished = False
        if self._current_setup_backup_task_processor is not None:
            finished = process_req_and_remove_sub_proc_if_its_finished(
                str_request, self._current_setup_backup_task_processor,
                self._remove_setting_up_subproc)
        elif str_request == "back":
            self._state = CreatingTaskState.START
            return True
        elif str_request == "help":
            self._sender.send_text(self.help)
            return False
        else:
            for processor in self._args_provider.\
                    get_setup_backup_task_processors(
                    current_task=self._current_backup_task_to_setup,
                    sender=self._sender,
                    args_provider=self._args_provider):
                if processor.fit_for_request(str_request):
                    self._current_setup_backup_task_processor = processor
                    finished = process_req_and_remove_sub_proc_if_its_finished(
                        str_request, self._current_setup_processor,
                        self._remove_setting_up_subproc)
                    break
            else:
                self._send_i_dont_understand()
        if finished:
            self._state = CreatingTaskState.START
        return finished

    def _process_request_setup_restore_task_state(self, str_request):
        finished = False
        if self._current_setup_restore_task_processor is not None:
            finished = process_req_and_remove_sub_proc_if_its_finished(
                str_request, self._current_setup_restore_task_processor,
                self._remove_restore_file_subproc)
        else:
            for processor in self._args_provider.\
                    get_setup_restore_task_processors(
                    current_task=self._current_restore_task_to_setup,
                    sender=self._sender,
                    args_provider=self._args_provider):
                if processor.fit_for_request(str_request):
                    self._current_setup_restore_task_processor = processor
                    finished = process_req_and_remove_sub_proc_if_its_finished(
                        str_request, processor,
                        self._remove_restore_file_subproc)
                    break
            else:
                self._send_i_dont_understand()
        if finished:
            self._state = CreatingTaskState.START
        return finished

    def _send_i_dont_understand(self):
        self._sender.send_text("Не понял запрос. Справка: help")

    def _send_backup_tasks_list(self):
        self._sender.send_text("Задачи бэкапа:")
        self._send_tasks(self._program_model.get_backup_tasks_dict())

    def _send_restore_tasks_list(self):
        self._sender.send_text("Задачи восстановления")
        self._send_tasks(self._program_model.get_restore_tasks_dict())

    def _send_tasks(self, task_dict):
        if len(task_dict) != 0:
            rows_to_send = []
            counter = 1
            for name in task_dict.keys():
                rows_to_send.append(f"\t{counter}) {name}")
                counter += 1
            self._sender.send_text("\n".join(rows_to_send))
        else:
            self._sender.send_text("\tСписок пуст")

    def _remove_setting_up_subproc(self):
        self._current_setup_processor = None

    def _remove_restore_file_subproc(self):
        self._current_restore_files_processor = None

    # TODO
    @property
    def help(self):
        if self._state == CreatingTaskState.START:
            return """
Создание бэкапа:
    - create task task_name
Настройка бэкапа:
    - setup task task_name
Удаление бэкапа:
    - delete task task_name
Список бэкапов:
    - tasks list
Запустить бэкап:
    - launch backup task_name"""
        elif self._state == CreatingTaskState.SETUP_BACKUP_TASK:
            return """Доступные команды:
- add/remove file file_name/file_path
- add/remove destination destination_name"""
