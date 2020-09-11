from View.ConsoleView.message_sender import MessageSender


class ConsoleMessageSender(MessageSender):
    def send_text(self, text, end="\n"):
        print(text, end=end)
