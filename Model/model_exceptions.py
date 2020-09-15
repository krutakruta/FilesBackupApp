class TaskWithTheSameNameAlreadyExist(Exception):
    pass


class ThereIsNoTaskWithSuchName(Exception):
    pass


class GoogleDriveIsNotReadyToAuthorize(Exception):
    pass


class ThereIsNoSubPathLikeThatInGoogleDrive(Exception):
    pass
