from Model.BackupElements.i_backup_element import IBackupElement
from Utilities.useful_functions import check_type_decorator


class FileBackupElement(IBackupElement):
    def __init__(self, file_path=None):
        self._file_path = file_path
        self._include_flag = True

    def set_file_path(self, file_path):
        self._file_path = file_path

    def is_ready_for_backup(self):
        return self._file_path is not None

    @property
    def title(self):
        return self._file_path

    @property
    def type_description(self):
        return "Файл"

    @property
    def include_flag(self):
        return self._include_flag

    @include_flag.setter
    @check_type_decorator(bool)
    def include_flag(self, value):
        self._include_flag = value
