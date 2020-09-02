from abc import abstractmethod


class MessageSender:
    @abstractmethod
    def send_text(self, text):
        raise NotImplementedError()