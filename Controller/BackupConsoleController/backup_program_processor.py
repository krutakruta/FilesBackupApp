from Controller.BackupConsoleController.processor import Processor


class BackupProgramProcessor(Processor):
    def __init__(self, current_backup_task, sender, args_provider):
        self._current_backup_task = current_backup_task
        self._sender = sender
        self._args_provider = args_provider
