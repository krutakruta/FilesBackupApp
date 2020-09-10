from Model.backup_program_model import BackupProgramModel
from Utilities.ArgsProvider.args_provider import ArgsProvider
from Controller.BackupConsoleController.MessageProcessors.\
    main_processor import MainProcessor
from Controller.BackupConsoleController.\
    backup_console_controller import BackupConsoleController
from View.ConsoleView.console_message_sender import ConsoleMessageSender
import sys


def launch_console_mode(model):
    message_sender = ConsoleMessageSender()
    args_provider = ArgsProvider()
    controller = BackupConsoleController(
        model, MainProcessor(message_sender, model, args_provider))
    controller.start_messaging()


def main():
    launch_console_mode(BackupProgramModel())


if __name__ == "__main__":
    main()