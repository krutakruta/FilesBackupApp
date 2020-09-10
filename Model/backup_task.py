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

    def remove_backup_element(self, element):
        self._backup_elements.remove(element)

    @check_type_decorator(IBackupDestination)
    def add_destination(self, destination):
        self._destination.append(destination)

    @check_type_decorator(str)
    def remove_destination(self, description):
        self._destination.remove(
            next(iter([d for d in self._destination
                       if d.description == description])))

    @property
    def name(self):
        return self._name
