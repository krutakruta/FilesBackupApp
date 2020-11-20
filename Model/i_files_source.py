from abc import abstractmethod


class IFilesSource:
    @property
    @abstractmethod
    def source_title(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def source_description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def include_source(self):
        raise NotImplementedError()

    @abstractmethod
    def add_source_sub_path_to_restore(self, sub_path):
        raise NotImplementedError()

    @abstractmethod
    def add_destination_sub_path_to_restore(self, sub_path):
        raise NotImplementedError()

    @abstractmethod
    def restore(self, source_sub_path, destination_sub_path):
        raise NotImplementedError()
