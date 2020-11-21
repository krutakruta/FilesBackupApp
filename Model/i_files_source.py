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

    @abstractmethod
    def set_destination_sub_path_to_restore(self, sub_path):
        raise NotImplementedError()

    @abstractmethod
    def restore(self, element):
        raise NotImplementedError()
