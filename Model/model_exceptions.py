class ProgramException(Exception):
    def __init__(self, message=None, *args, **kwargs):
        self.message = message
        super().__init__(*args, **kwargs)


class TaskWithTheSameNameAlreadyExist(ProgramException):
    pass


class ThereIsNoTaskWithSuchName(ProgramException):
    pass


class NotReadyToAuthorizeError(ProgramException):
    pass


class ThereIsNoSubPathLikeThatInGoogleDrive(ProgramException):
    pass


class TaskError(ProgramException):
    pass


class InvalidAuthCodeError(ProgramException):
    pass


class InvalidClientError(ProgramException):
    pass


class GoogleDriveError(ProgramException):
    pass


class YandexDiskError(ProgramException):
    pass
