from abc import abstractmethod


class IBackupDestination:
    @property
    @abstractmethod
    def title(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def type_description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def include(self):
        raise NotImplementedError()

    @abstractmethod
    def deliver_element(self, element):
        raise NotImplementedError()
