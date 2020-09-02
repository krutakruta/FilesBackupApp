from Controller.BackupConsoleController.MessageProcessors.processor import Processor
from re import match


class FileProcessor(Processor):
    def __init__(self, current_backup_task):
        self._current_backup_task = current_backup_task

    def fit_for_request(self, string):
        return match("add file /w/W*|remove file /w/W*") is not None

    def process_request(self, string):
        pass

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

