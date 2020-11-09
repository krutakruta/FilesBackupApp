from Controller.BackupConsoleController.BackupElementsProcessors.file_processor import FileProcessor
from Controller.BackupConsoleController.google_drive_processor import GoogleDriveProcessor
from Controller.BackupConsoleController.yandex_disk_processor import YandexDiskDestinationProcessor
from Utilities.ArgsProvider.i_args_provider import IArgsProvider
from Controller.BackupConsoleController.RestoreElementsProcessors.\
    files_restore_processor import FilesRestoreProcessor


class ArgsProvider(IArgsProvider):
    def get_all_setting_up_processors(self, *args, **kwargs):
        return (self.get_all_backup_elements_processors(*args, **kwargs) +
                self.get_all_destination_processors(*args, **kwargs))

    def get_all_destination_processors(self, *args, **kwargs):
        return [GoogleDriveProcessor(*args, **kwargs),
                YandexDiskDestinationProcessor(*args, **kwargs)]

    def get_all_backup_elements_processors(self, *args, **kwargs):
        return [FileProcessor(*args, **kwargs)]

    def get_all_restore_files_processors(self, *args, **kwargs):
        return [FilesRestoreProcessor(*args, **kwargs)]
