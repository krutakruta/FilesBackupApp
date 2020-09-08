from Utilities.useful_functions import check_type_decorator
from Model.BackupElements.i_backup_element import IBackupElement
from Model.BackupDestination.i_backup_destination import IBackupDestination


class BackupTask:
    def __init__(self, name):
        self._backup_elements = []
        self._destination = []
        self._name = name

    @check_type_decorator(IBackupElement)
    def add_backup_element(self, element):
        self._backup_elements.append(element)

    @check_type_decorator(IBackupDestination)
    def add_destination(self, destination):
        self._destination.append(destination)

    @property
    def name(self):
        return self._name
