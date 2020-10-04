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


class BadConfirmationCodeError(Exception):
    pass


class BadTokenError(Exception):
    pass


class YandexDiskError(Exception):
    pass
