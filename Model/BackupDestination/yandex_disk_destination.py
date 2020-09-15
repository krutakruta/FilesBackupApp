from Model.BackupDestination.i_backup_destination import IBackupDestination


class YandexDiskDestination(IBackupDestination):
    def __init__(self, args_provider, title="YandexDisk"):
        self._args_provider = args_provider
        self._title = title
        self._include_flag = True
        self._sub_path = "/"

    @property
    def title(self):
        return self._title

    @property
    def type_description(self):
        return "Yandex Disk облако"

    @property
    def include(self):
        return self._include_flag

    def deliver_element(self, element):
        pass
