from Controller.BackupConsoleController.DestinationProcessors.\
    google_drive_destination_processor import \
    GoogleDriveDestinationProcessor
from Controller.BackupConsoleController.DestinationProcessors.\
    main_destination_processor import MainDestinationProcessor
from Controller.BackupConsoleController.DestinationProcessors\
    .yandex_disk_destination_processor import YandexDiskDestinationProcessor
from Controller.BackupConsoleController.SourceProcessors.\
    google_drive_source_processor import GoogleDriveSourceProcessor
from Controller.BackupConsoleController.SourceProcessors.\
    main_source_processor import MainSourceProcessor
from Controller.BackupConsoleController.SourceProcessors.\
    yandex_disk_source_processor import YandexDiskSourceProcessor
from Utilities.ArgsProvider.i_args_provider import IArgsProvider


class ArgsProvider(IArgsProvider):
    def get_setup_backup_task_processors(self, **kwargs):
        return self.get_main_destination_processors(**kwargs)

    def get_main_destination_processors(self, **kwargs):
        return [MainDestinationProcessor(**kwargs)]

    def get_destination_processors(self, **kwargs):
        return [GoogleDriveDestinationProcessor(**kwargs),
                YandexDiskDestinationProcessor(**kwargs)]

    def get_setup_restore_task_processors(self, **kwargs):
        return self.get_main_source_processors(**kwargs)

    def get_main_source_processors(self, **kwargs):
        return [MainSourceProcessor(**kwargs)]

    def get_source_processors(self, **kwargs):
        return [GoogleDriveSourceProcessor(**kwargs),
                YandexDiskSourceProcessor(**kwargs)]
