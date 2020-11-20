from abc import abstractmethod


class IGoogleDriveBackupable:
    @abstractmethod
    def backup_to_google_drive(self, google_service, dst_path, *args, **kwargs):
        raise NotImplementedError()
