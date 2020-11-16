from Controller.BackupConsoleController.BackupElementsProcessors.\
    file_processor import FileProcessor
from Controller.BackupConsoleController.DestinationProcessors.\
    google_drive_destination_processor import \
    GoogleDriveDestinationProcessor
from Controller.BackupConsoleController.DestinationProcessors.\
    main_destination_processor import MainDestinationProcessor
from Controller.BackupConsoleController.DestinationProcessors\
    .yandex_disk_destination_processor import YandexDiskDestinationProcessor
from Utilities.ArgsProvider.i_args_provider import IArgsProvider
from Controller.BackupConsoleController.RestoreElementsProcessors.\
    files_restore_processor import FilesRestoreProcessor


class ArgsProvider(IArgsProvider):
    def get_all_setup_processors(self, **kwargs):
        return (self.get_all_backup_elements_processors(**kwargs) +
                self.get_all_destination_processors(**kwargs))

    def get_all_destination_processors(self, **kwargs):
        return [GoogleDriveDestinationProcessor(**kwargs),
                YandexDiskDestinationProcessor(**kwargs),
                MainDestinationProcessor(**kwargs)]

    def get_all_backup_elements_processors(self, **kwargs):
        return [FileProcessor(**kwargs)]

    def get_all_restore_files_processors(self, **kwargs):
        return [FilesRestoreProcessor(**kwargs)]
