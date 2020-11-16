from Controller.BackupConsoleController.processor import Processor


class BackupProgramProcessor(Processor):
    def __init__(self, current_task, sender, args_provider, **kwargs):
        self._current_task = current_task
        self._sender = sender
        self._args_provider = args_provider
