from abc import abstractmethod


class IBackupElement:
    @abstractmethod
    def is_ready_for_backup(self):
        raise NotImplementedError()

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
    def include_flag(self):
        raise NotImplementedError()