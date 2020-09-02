class BackupConsoleController:
    def __init__(self, backup_program_model, all_processors):
        self._backup_program_model = backup_program_model
        self._current_processor = None
        self._all_processors = all_processors

    def start_messaging(self):
        while True:
            message = input()
            if message == "exit":
                return
            self._process_request(message)

    def _process_request(self, string):
        if self._current_processor is not None:
            return self._process_request_and_remove_processor_if_its_finished(
                string)
        for processor in self._all_processors:
            if processor.fit_for_request(string):
                self._process_request_and_remove_processor_if_its_finished(
                    string)

    def _process_request_and_remove_processor_if_its_finished(self, string):
        finished = self._current_processor.process_request(string)
        self._current_processor = \
            None if finished else self._current_processor
        return finished
