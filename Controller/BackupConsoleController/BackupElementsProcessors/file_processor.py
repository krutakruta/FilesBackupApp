from Controller.BackupConsoleController\
    .backup_program_processor import BackupProgramProcessor
from re import match
from Model.BackupElements.file_backup_el import FileBackupElement


class FileProcessor(BackupProgramProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fit_for_request(self, str_request):
        return match("add file.*|remove file.*", str_request) is not None

    def process_request(self, str_request):
        if str_request == "back":
            return True
        command = match(r"(\w+) file.*", str_request).group(1)
        path_match = match(r"\w+ file (.+)", str_request)
        if command == "add":
            if path_match is None:
                self._sender.send_text("Вы не задали имя файла")
                return False
            self._current_task.add_backup_element(
                FileBackupElement(path_match.group(1)))
            self._sender.send_text("Файл добавлен")
            return True
        elif command == "remove":
            self._current_task.remove_backup_element(
                path_match.group(1))
            return True
        else:
            self._sender.send_text("Неправильный запрос. Справка: help")
        return False


    @property
    def help(self):
        return """Добавление/удаление файлов:
-add file path
-remove file path/index_in_list
Например: *add file C:/Users/best_user/some_file
*add file C:/Users/best_user/*.txt
*add file C:/Users/best_user/*.*
*remove file C:/Users/best_user/some_file
*remove file 2

help: справка
back: вернуться"""

