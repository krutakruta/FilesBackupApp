from Controller.BackupConsoleController.MessageProcessors\
    .file_processor import FileProcessor
from Controller.BackupConsoleController.MessageProcessors\
    .google_drive_destination_processor import GoogleDriveDestinationProcessor
from Utilities.ArgsProvider.i_args_provider import IArgsProvider


class ArgsProvider(IArgsProvider):
    def get_all_destination_processors(self, *args, **kwargs):
        return [GoogleDriveDestinationProcessor(*args, **kwargs)]

    def get_all_backup_elements_processors(self, *args, **kwargs):
        return [FileProcessor(*args, **kwargs)]
