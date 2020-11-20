from abc import abstractmethod


class IRestoreElement:
    @property
    @abstractmethod
    def restore_title(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def restore_type_description(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def restore_log(self):
        raise NotImplementedError()
