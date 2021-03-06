from abc import abstractmethod


class IBackupElement:
    @abstractmethod
    def is_ready_for_backup(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def backup_title(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def type_description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def backup_log(self):
        raise NotImplementedError()
