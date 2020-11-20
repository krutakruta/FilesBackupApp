from Model.model_exceptions import TaskError
from Utilities.useful_functions import check_type_decorator
from Model.BackupElements.i_backup_element import IBackupElement
from Model.i_backup_destination import IBackupDestination


class BackupTask:
    def __init__(self, name):
        self._backup_elements = []
        self._destination = []
        self._name = name

    @check_type_decorator(IBackupElement)
    def add_backup_element(self, element):
        if element in self._backup_elements:
            raise TaskError(
                "Элемент для бэкапа с таким названием уже существует")
        self._backup_elements.append(element)

    @check_type_decorator(str)
    def remove_backup_element(self, title):
        try:
            self._backup_elements.remove(
                next(iter((el for el in self._backup_elements
                           if el.destination_title == title))))
        except StopIteration:
            raise TaskError(
                "Элементов для бэкапа с таким название не существует")

    @check_type_decorator(IBackupDestination)
    def add_destination(self, destination):
        if destination.destination_title in (title for title in self._destination):
            raise TaskError(
                "Назначение с таким названием уже существует")
        self._destination.append(destination)

    @check_type_decorator(str)
    def remove_destination(self, title):
        try:
            self._backup_elements.remove(
                next(iter((d for d in self._destination
                           if d.destination_title == title))))
        except StopIteration:
            raise TaskError("Назначения с таким названием не существует")

    def launch_backup(self):
        result_log = []
        for destination in self._destination:
            for backup_element in self._backup_elements:
                result_log.append(destination.deliver_element(backup_element))
        return result_log

    @property
    def name(self):
        return self._name
