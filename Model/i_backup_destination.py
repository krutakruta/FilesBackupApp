from abc import abstractmethod


class IBackupDestination:
    @property
    @abstractmethod
    def destination_title(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def destination_description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def include_destination(self):
        raise NotImplementedError()

    @abstractmethod
    def add_sub_path_to_backup(self, sub_path):
        raise NotImplementedError()

    @abstractmethod
    def deliver_element(self, element):
        raise NotImplementedError()
