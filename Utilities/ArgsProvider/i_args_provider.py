from abc import abstractmethod
from Controller.BackupConsoleController.MessageProcessors\
    .google_drive_destination_processor import GoogleDriveDestinationProcessor


class IBackupElementProcessorsProvider:
    @abstractmethod
    def get_all_backup_elements_processors(self):
        raise NotImplementedError()


class IDestinationProcessorsProvider:
    @abstractmethod
    def get_all_destination_processors(self):
        raise NotImplementedError()


class IArgsProvider(IDestinationProcessorsProvider,
                    IBackupElementProcessorsProvider):
    pass
