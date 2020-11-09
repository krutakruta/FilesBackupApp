from abc import abstractmethod


class IBackupDestination:
    @property
    @abstractmethod
    def title(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def include(self):
        raise NotImplementedError()

    @abstractmethod
    def add_sub_path(self, sub_path):
        raise NotImplementedError()

    @abstractmethod
    def remove_sub_path(self, sub_path):
        raise NotImplementedError()

    @abstractmethod
    def deliver_element(self, element):
        raise NotImplementedError()
