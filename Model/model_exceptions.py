class TaskWithTheSameNameAlreadyExist(Exception):
    pass


class ThereIsNoTaskWithSuchName(Exception):
    pass


class NotReadyToAuthorizeError(Exception):
    pass


class ThereIsNoSubPathLikeThatInGoogleDrive(Exception):
    pass


class BackupTaskError(Exception):
    pass


class InvalidAuthCodeError(Exception):
    pass


class InvalidClientError(Exception):
    pass


class GoogleDriveError(Exception):
    pass


class YandexDiskError(Exception):
    pass
