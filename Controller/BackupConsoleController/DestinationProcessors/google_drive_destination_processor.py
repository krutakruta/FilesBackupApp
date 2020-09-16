from Controller.BackupConsoleController\
    .backup_program_processor import BackupProgramProcessor
from Model.BackupDestination\
    .google_drive_destination import GoogleDriveDestination
from enum import Enum
import re


class GDDProcessorState(Enum):
    JUST_CREATED = 0
    NAMING = 1
    CLIENT_ID = 2
    CLIENT_SECRET = 3
    SUB_PATH = 4
    AUTHORIZED = 5


class GoogleDriveDestinationProcessor(BackupProgramProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_destination = None
        self._state = GDDProcessorState.JUST_CREATED

    def fit_for_request(self, str_request):
        return re.match(r"add destination googleDrive|"
                        r"remove destination googleDrive.*",
                        str_request, re.IGNORECASE) is not None

    def process_request(self, str_request):
        if str_request == "back":
            self._check_current_destination()
            return True
        elif str_request == "help":
            self._sender.send_text(self.help)
        elif self._state == GDDProcessorState.JUST_CREATED:
            command = re.match(r"(\w+) destination googleDrive.*", str_request,
                               re.IGNORECASE).group(1)
            if command == "remove":
                self._remove_destination(str_request)
                return True
            else:
                self._current_destination = GoogleDriveDestination(
                    self._args_provider)
                self._current_backup_task.add_destination(
                    self._current_destination)
                self._sender.send_text("Введите название: ", end="")
                self._state = GDDProcessorState.NAMING
        elif self._state == GDDProcessorState.NAMING:
            self._current_destination.title = re.match(r"(.+)", str_request)\
                .group(1)
            self._sender.send_text("Введите подпуть(по умолчанию '/'): ",
                                   end="")
            self._state = GDDProcessorState.SUB_PATH
        elif self._state == GDDProcessorState.SUB_PATH:
            sub_path = re.match(r"(.*)", str_request).group(1)
            self._current_destination.sub_path =\
                (sub_path if sub_path != ""
                 else self._current_destination.sub_path)
            self._sender.send_text("Введите client_id: ", end="")
            self._state = GDDProcessorState.CLIENT_ID
        elif self._state == GDDProcessorState.CLIENT_ID:
            self._current_destination.client_id = re.match(
                r"(.+)", str_request).group(1)
            self._sender.send_text("Введите client_secret: ", end="")
            self._state = GDDProcessorState.CLIENT_SECRET
        elif self._state == GDDProcessorState.CLIENT_SECRET:
            self._current_destination.client_secret = re.match(
                r"(.+)", str_request).group(1)
            self._current_destination.authorize()
            self._sender.send_text("Вы авторизованы. Google drive добавлен")
            self._state = GDDProcessorState.AUTHORIZED
        return False

    def _remove_destination(self, str_request):
        match_res = re.match(r"remove destination googleDrive (.+)",
                             str_request, re.IGNORECASE)
        if match_res is None:
            self._sender.send_text("Вы не задали название")
        else:
            self._current_backup_task.remove_destination(match_res.group(1))

    def _check_current_destination(self):
        if self._current_destination is None:
            return
        if not self._current_destination.ready_to_authorize():
            self._current_backup_task.remove_destination(
                self._current_destination)
            self._current_destination = None
            self._sender.send_text("Google Drive 'удален', т.к. не был настроен")

    @property
    def help(self):
        return """
Для авторизации в Google Drive необходимы следующие параметры:
- client_id
- client_secret,
которые предоставляются при подключеннии google drive api"""