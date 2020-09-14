from Model.BackupElements.i_backup_element import IBackupElement
from Model.BackupElements\
    .i_google_drive_backupable import IGoogleDriveBackupable
from Utilities.useful_functions import check_type_decorator
from googleapiclient.http import MediaFileUpload


class FileBackupElement(IBackupElement, IGoogleDriveBackupable):
    def __init__(self, file_path=None):
        self._file_path = file_path
        self._include_flag = True

    def set_file_path(self, file_path):
        self._file_path = file_path

    def is_ready_for_backup(self):
        return self._file_path is not None

    def backup_to_google_drive(self, google_service, sub_path,
                               *args, **kwargs):
        folder_name = self._parse_path_and_get_path_sheet(sub_path)
        if sub_path == "/":
            parent = []
        else:
            parent = google_service.files().list(
                q=f"mimeType='application/vnd.google-apps.folder' "
                  f"and name = {folder_name}",
                fields="files(id)").execute()["files"]
            if not parent:
                return f"GoogleDrive: такого подпути не существует {sub_path}"
        file_metadata = {
            "name": self._parse_path_and_get_path_sheet(self._file_path),
            "parents": [parent.pop["id"]]
        }
        try:
            media = MediaFileUpload(self._file_path, resumable=True)
            google_service.files().create(body=file_metadata, media_body=media)
        except FileNotFoundError:
            return f"GoogleDrive: Файл {self._file_path} не найден"
        except PermissionError:
            return f"GoogleDrive: Ошибка доступа к файлу {self._file_path}"
        except Exception:
            return f"GoogleDrive: неизвестная ошибка" \
                   f"при попытке отправить файл {self._file_path}"
        return f"GoogleDrive: {self._file_path} success"

    def _get_parent_id(self, sub_path):
        pass

    def _parse_path_and_get_path_sheet(self, path):
        split = path.replace("\\", "/").split("/")
        if len(split) > 1:
            return split[-1] if split[-1] != "" else split[-2]
        return split[0]

    @property
    def title(self):
        return self._file_path

    @property
    def type_description(self):
        return "Файл"

    @property
    def include_flag(self):
        return self._include_flag

    @include_flag.setter
    @check_type_decorator(bool)
    def include_flag(self, value):
        self._include_flag = value
