from abc import abstractmethod


class ISetupRestoreTaskProcessorsProvider:
    @abstractmethod
    def get_setup_restore_task_processors(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_main_source_processors(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_source_processors(self, **kwargs):
        raise NotImplementedError()


class ISetupBackupTaskProcessorsProvider:
    @abstractmethod
    def get_setup_backup_task_processors(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_main_destination_processors(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_destination_processors(self, **kwargs):
        raise NotImplementedError()


class IArgsProvider(ISetupRestoreTaskProcessorsProvider,
                    ISetupBackupTaskProcessorsProvider):
    pass
