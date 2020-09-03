from Utilities.useful_functions import check_type_decorator
from Model.BackupElements.i_backup_element import IBackupElement


class BackupTask:
    def __init__(self, name):
        self._backup_elements = []
        self._name = name

    @check_type_decorator(IBackupElement)
    def add_backup_element(self, element):
        self._backup_elements.append(element)

    @property
    def name(self):
        return self._name
