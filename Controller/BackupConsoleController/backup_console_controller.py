class BackupConsoleController:
    def __init__(self, backup_program_model, main_processor):
        self._backup_program_model = backup_program_model
        self._main_processor = main_processor

    def start_messaging(self):
        print("Python task backup program. Справка: help")
        while not self._main_processor.process_request(input()):
            pass
