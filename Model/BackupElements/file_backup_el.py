import re

from Model.Clouds.google_drive_cloud import GoogleDriveCloud
from Model.BackupElements.i_backup_element import IBackupElement
from Model.BackupElements \
    .i_google_drive_backupable import IGoogleDriveBackupable
from Model.BackupElements.i_yandex_disk_backupable import IYandexDiskBackupable
from Model.model_exceptions import ThereIsNoSubPathLikeThatInGoogleDrive
from Utilities.useful_functions import check_type_decorator
from googleapiclient.http import MediaFileUpload
from Utilities.useful_functions import parse_path_and_get_path_sheet


class FileBackupElement(IBackupElement, IGoogleDriveBackupable,
                        IYandexDiskBackupable):
    def __init__(self, file_path=None):
        self._file_path = file_path
        self._include_flag = True
        self._backup_log = []

    def set_file_path(self, file_path):
        self._file_path = file_path

    def is_ready_for_backup(self):
        return self._file_path is not None

    def backup_to_yandex_disk(self, yandex_service, sub_path, **kwargs):
        try:
            yandex_service.upload(
                self._file_path,
                "/".join(list(filter(lambda i: i != "",
                                     sub_path.replace("\\", "/").split("/"))) +
                         [parse_path_and_get_path_sheet(self._file_path)]),
                overwrite=True)
        except Exception:
            self._backup_log.append(
                f"Yandex Disk: Неизвестная ошибка при попытке бэкапа"
                f"файла {self._file_path}")
        else:
            self._backup_log.append(
                f"Yandex Disk: {self._file_path} success")

    def backup_to_google_drive(self, google_service, sub_path,
                               *args, **kwargs):
        try:
            target_folders_id = list(
                map(lambda folder: folder["id"],
                    GoogleDriveCloud.get_target_folders_of_not_root_path_in_google_drive(
                        google_service, sub_path)))
            file_metadata = {
                "name": parse_path_and_get_path_sheet(self._file_path),
                "parents": target_folders_id
            }
            media = MediaFileUpload(self._file_path, resumable=True)
            google_service.files().create(
                body=file_metadata, media_body=media, fields="id").execute()
        except ThereIsNoSubPathLikeThatInGoogleDrive:
            self._backup_log.append(
                f"GoogleDrive: подпути {sub_path} в"
                f"Google Drive не существует")
        except FileNotFoundError:
            self._backup_log.append(
                f"GoogleDrive: Файл {self._file_path} не найден")
        except PermissionError:
            self._backup_log.append(
                f"GoogleDrive: Ошибка доступа к файлу {self._file_path}")
        except Exception:
            self._backup_log.append(
                f"GoogleDrive: неизвестная ошибка"
                f"при попытке отправить файл {self._file_path}")
        else:
            self._backup_log.append(f"GoogleDrive: {self._file_path} success")

    @property
    def title(self):
        return self._file_path

    @property
    def type_description(self):
        return "Файл"

    @property
    def include_flag(self):
        return self._include_flag

    @property
    def backup_log(self):
        return self._backup_log

    @include_flag.setter
    @check_type_decorator(bool)
    def include_flag(self, value):
        self._include_flag = value
