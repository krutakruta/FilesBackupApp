from Controller.BackupConsoleController.MessageProcessors\
    .processor import Processor
from re import match
from Model.BackupElements.file_backup_el import FileBackupElement


class FileProcessor(Processor):
    def __init__(self, current_backup_task, sender, args_provider):
        self._current_backup_task = current_backup_task
        self._sender = sender
        self._args_provider = args_provider

    def fit_for_request(self, str_request):
        return match("add file .*|remove file .*", str_request) is not None

    def process_request(self, str_request):
        command = match(r"(\w)+ file (.+) .*", str_request).group(1)
        path_match = match(r"\w+ file (.+) .*", str_request)
        if command == "add":
            if path_match is None:
                self._sender.send_text("Задайте путь к файлу")
            else:
                self._current_backup_task.add_backup_element(
                    FileBackupElement(path_match.group(1)))
            return True
        elif command == "remove":
            pass
        else:
            self._sender.send_text("Неправильный запрос")

    @property
    def help(self):
        return """Добавление/удаление файлов:\n
            \t-add file path\n
            \t-remove file path/index_in_list\n
            Например: *add file C:/Users/best_user/some_file
                      *add file C:/Users/best_user/*.txt
                      *add file C:/Users/best_user/*.*
                      *remove file C:/Users/best_user/some_file
                      *remove file 2"""

