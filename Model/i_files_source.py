from abc import abstractmethod


class IFilesSource:
    @property
    @abstractmethod
    def source_title(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self):
        raise NotImplementedError()

    def include(self):
        raise NotImplementedError()
