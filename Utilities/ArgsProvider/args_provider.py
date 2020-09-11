from Controller.BackupConsoleController.BackupElementsProcessors.file_processor import FileProcessor
from Controller.BackupConsoleController.DestinationProcessors.google_drive_destination_processor import GoogleDriveDestinationProcessor
from Utilities.ArgsProvider.i_args_provider import IArgsProvider


class ArgsProvider(IArgsProvider):
    def get_all_setting_up_processors(self, *args, **kwargs):
        return (self.get_all_backup_elements_processors(*args, **kwargs) +
                self.get_all_destination_processors(*args, **kwargs))

    def get_all_destination_processors(self, *args, **kwargs):
        return [GoogleDriveDestinationProcessor(*args, **kwargs)]

    def get_all_backup_elements_processors(self, *args, **kwargs):
        return [FileProcessor(*args, **kwargs)]
