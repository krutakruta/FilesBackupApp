from abc import abstractmethod


class Processor:
    @abstractmethod
    def fit_for_request(self, str_request):
        raise NotImplementedError()

    @abstractmethod
    def process_request(self, str_request):
        raise NotImplementedError()

    @abstractmethod
    def is_finished(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def help(self):
        raise NotImplementedError()
