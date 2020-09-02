from Model.backup_task import BackupTask


class BackupProgramModel:
    def __init__(self):
        self._tasks = []

    def create_task(self):
        self._tasks.append(BackupTask())

    def get_tasks_list(self):
        return self._tasks
