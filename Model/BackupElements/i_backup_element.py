from abc import abstractmethod


class IBackupElement:
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