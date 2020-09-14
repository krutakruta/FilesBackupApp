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

    @check_type_decorator(str)
    def remove_backup_element(self, element_title):
        self._backup_elements.remove(
            next(iter([el for el in self._backup_elements
                       if el.title == element_title])))

    @check_type_decorator(IBackupDestination)
    def add_destination(self, destination):
        self._destination.append(destination)

    @check_type_decorator(str)
    def remove_destination(self, destination_title):
        self._destination.remove(
            next(iter([d for d in self._destination
                       if d.title == destination_title])))

    def launch_backup(self):
        result_log = set()
        for destination in self._destination:
            for backup_element in self._backup_elements:
                result_log.add(destination.deliver_element(backup_element))
        return result_log

    @property
    def name(self):
        return self._name
