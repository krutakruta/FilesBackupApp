from Model.BackupElements.i_backup_element import IBackupElement
from Utilities.useful_functions import check_type_decorator


class FileBackupElement(IBackupElement):
    def __init__(self):
        self._file_path = None
        self._include_flag = True

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
