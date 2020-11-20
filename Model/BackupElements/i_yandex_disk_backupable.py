from abc import abstractmethod


class IYandexDiskBackupable:
    @abstractmethod
    def backup_to_yandex_disk(self, yandex_service, dst_path, **kwargs):
        raise NotImplementedError()
