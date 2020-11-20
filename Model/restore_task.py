from Model.i_files_source import IFilesSource
from Model.model_exceptions import TaskError
from Utilities.useful_functions import check_type_decorator


class RestoreTask:
    def __init__(self, name):
        self._name = name
        self._source = []

    @check_type_decorator(IFilesSource)
    def add_source(self, source):
        if source.source_title in self._source:
            raise TaskError("Источник с таким названием уже существует")
        self._source.append(source)

    @check_type_decorator(str)
    def remove_source(self, title):
        try:
            self._source.remove(
                next(iter((d for d in self._source
                           if d.source_title == title))))
        except StopIteration:
            raise TaskError("Источника с таким названием не существует")

    def launch(self):
        result_log = []
        for source in self._source:
            pass

    @property
    def name(self):
        return self._name
