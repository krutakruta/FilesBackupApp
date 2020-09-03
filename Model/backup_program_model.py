from Model.backup_task import BackupTask
from Model.model_exceptions import TaskWithTheSameNameAlreadyExist,\
    ThereIsNoTaskWithSuchName


class BackupProgramModel:
    def __init__(self):
        self._tasks = {}

    def create_task(self, task_name):
        if task_name in self._tasks:
            raise TaskWithTheSameNameAlreadyExist()
        self._tasks[task_name] = BackupTask(task_name)

    def delete_task(self, task_name):
        if task_name not in self._tasks:
            raise ThereIsNoTaskWithSuchName
        del self._tasks[task_name]

    def get_tasks_dict(self):
        return self._tasks
