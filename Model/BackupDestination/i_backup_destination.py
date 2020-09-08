from abc import abstractmethod


class IBackupDestination:
    @property
    @abstractmethod
    def description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def type_description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def include(self):
        raise NotImplementedError()
