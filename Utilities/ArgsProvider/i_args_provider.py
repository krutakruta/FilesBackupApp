from abc import abstractmethod


class IBackupElementProcessorsProvider:
    @abstractmethod
    def get_all_backup_elements_processors(self):
        raise NotImplementedError()


class IDestinationProcessorsProvider:
    @abstractmethod
    def get_all_destination_processors(self):
        raise NotImplementedError()


class ISettingUpProcessorsProvider:
    @abstractmethod
    def get_all_setting_up_processors(self):
        raise NotImplementedError()


class IArgsProvider(IDestinationProcessorsProvider,
                    IBackupElementProcessorsProvider,
                    ISettingUpProcessorsProvider):
    pass
