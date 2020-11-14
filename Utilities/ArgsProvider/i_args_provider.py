from abc import abstractmethod


class IBackupElementProcessorsProvider:
    @abstractmethod
    def get_all_backup_elements_processors(self):
        raise NotImplementedError()


class IDestinationProcessorsProvider:
    @abstractmethod
    def get_all_destination_processors(self):
        raise NotImplementedError()


class ISetupProcessorsProvider:
    @abstractmethod
    def get_all_setup_processors(self):
        raise NotImplementedError()


class IRestoreFilesProcessorsProvider:
    @abstractmethod
    def get_all_restore_files_processors(self):
        raise NotImplementedError()


class IArgsProvider(IDestinationProcessorsProvider,
                    IBackupElementProcessorsProvider,
                    ISetupProcessorsProvider,
                    IRestoreFilesProcessorsProvider):
    pass
