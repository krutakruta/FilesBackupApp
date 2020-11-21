from Model.backup_task import BackupTask
from Model.restore_task import RestoreTask
from Model.model_exceptions import TaskWithTheSameNameAlreadyExist,\
    ThereIsNoTaskWithSuchName


class ProgramModel:
    def __init__(self):
        self._backup_tasks = {}
        self._restore_tasks = {}

    def create_backup_task(self, task_name):
        if task_name in self._backup_tasks:
            raise TaskWithTheSameNameAlreadyExist()
        self._backup_tasks[task_name] = BackupTask(task_name)

    def delete_backup_task(self, task_name):
        self._backup_tasks.pop(task_name, None)

    def launch_backup(self, task_name):
        if task_name not in self._backup_tasks:
            raise ThereIsNoTaskWithSuchName()
        return self._backup_tasks[task_name].launch_backup()

    def launch_restore(self, task_name):
        if task_name not in self._restore_tasks:
            raise ThereIsNoTaskWithSuchName()
        return self._restore_tasks[task_name].restore()

    def create_restore_task(self, task_name):
        if task_name in self._restore_tasks:
            raise TaskWithTheSameNameAlreadyExist()
        self._restore_tasks[task_name] = RestoreTask(task_name)

    def delete_restore_task(self, task_name):
        self._restore_tasks.pop(task_name, None)

    def get_backup_tasks_dict(self):
        return self._backup_tasks

    def get_restore_tasks_dict(self):
        return self._restore_tasks
