from Utilities.useful_functions import check_type_decorator
from Model.BackupElements.i_backup_element import IBackupElement


class BackupTask:
    def __init__(self):
        self._backup_elements = []

    @check_type_decorator(IBackupElement)
    def add_backup_element(self, element):
        self._backup_elements.append(element)
