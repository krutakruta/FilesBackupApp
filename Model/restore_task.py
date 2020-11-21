from Model.model_exceptions import TaskError
from Utilities.useful_functions import check_type_decorator


class RestoreTask:
    def __init__(self, name):
        self._name = name
        self._source_and_elements = {}

    def add_source(self, source):
        if source.source_title in self._source_titles:
            raise TaskError("Источник с таким названием уже существует")
        self._source_and_elements[source] = []

    @check_type_decorator(str)
    def remove_source(self, title):
        if title not in self._source_titles:
            raise TaskError("Источника с таким названием не существует")
        self._source_and_elements.pop(self._get_source_by_title(title), None)

    def add_element_to_restore(self, element, source):
        if source.source_title not in self._source_titles:
            raise TaskError("Источника с таким названием не существует")
        if element in self._source_and_elements[source]:
            raise TaskError("Такой элемент уже присутствует")
        self._source_and_elements[source].append(element)

    def launch(self):
        result_log = []
        for source in self._source_and_elements.keys():
            for element in self._source_and_elements[source]:
                result_log.append(source.restore(element))
        return result_log

    def _get_source_by_title(self, title):
        for source in self._source_and_elements.keys():
            if source.source_title == title:
                return source
        return None

    @property
    def name(self):
        return self._name

    @property
    def _source_titles(self):
        return map(lambda source: source.source_title,
                   self._source_and_elements.keys())
