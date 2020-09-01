from abc import abstractmethod


class Processor:
    def __init__(self, sender):
        self._sender = sender

    @abstractmethod
    def fit_for_request(self, string):
        raise NotImplementedError()

    @abstractmethod
    def process_request(self, string):
        raise NotImplementedError()

    @property
    @abstractmethod
    def help(self):
        raise NotImplementedError()