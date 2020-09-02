from Model.backup_program_model import BackupProgramModel
from Controller.BackupConsoleController.MessageProcessors.\
    file_processor import FileProcessor
from Controller.BackupConsoleController.\
    backup_console_controller import BackupConsoleController
from View.ConsoleView.console_message_sender import ConsoleMessageSender
import sys


def get_all_message_processors(message_sender):
    return [FileProcessor(message_sender)]


def launch_console_mode(model):
    message_sender = ConsoleMessageSender()
    controller = BackupConsoleController(
        model, get_all_message_processors(message_sender))
    controller.start_messaging()


def main():
    if len(sys.argv) > 1:
        launch_console_mode(BackupProgramModel())


if __name__ == "__main__":
    main()