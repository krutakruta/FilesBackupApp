from Model.Clouds.google_drive_cloud import GoogleDriveCloud
from Model.BackupElements.i_backup_element import IBackupElement
from Model.BackupElements \
    .i_google_drive_backupable import IGoogleDriveBackupable
from Model.BackupElements.\
    i_yandex_disk_backupable import IYandexDiskBackupable
from Model.RestoreElements.\
    i_google_drive_recovering import IGoogleDriveRecovering
from Model.RestoreElements.i_restore_element import IRestoreElement
from Model.model_exceptions import ThereIsNoSubPathLikeThatInGoogleDrive
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from Utilities.useful_functions import parse_path_and_get_path_sheet


class File(IBackupElement, IRestoreElement,
           IGoogleDriveBackupable, IYandexDiskBackupable,
           IGoogleDriveRecovering):
    def __init__(self, file_path=None):
        self._file_path = file_path
        self._include_flag = True
        self._backup_log = []
        self._restore_log = []

    def set_file_path(self, file_path):
        self._file_path = file_path

    def is_ready_for_backup(self):
        return self._file_path is not None

    def backup_to_yandex_disk(self, yandex_service, dst_path, **kwargs):
        try:
            yandex_service.upload(
                self._file_path,
                "/".join(list(filter(lambda i: i != "",
                                     dst_path.replace("\\", "/").split("/"))) +
                         [parse_path_and_get_path_sheet(self._file_path)]),
                overwrite=True)
            return f"YandexDiskBackup: {self._file_path} успех"
        except Exception:
            return f"YandexDiskBackup: Неизвестная ошибка при попытке бэкапа " \
                   f"файла {self._file_path}"

    def backup_to_google_drive(self, google_service, dst_path,
                               *args, **kwargs):
        try:
            target_folders_id = []
            if dst_path != "/":
                target_folders_id = list(
                    map(lambda folder: folder["id"],
                        GoogleDriveCloud.get_target_folders_of_not_root_path_in_google_drive(
                            google_service, dst_path)))
            file_metadata = {
                "name": parse_path_and_get_path_sheet(self._file_path),
                "parents": target_folders_id
            }
            media = MediaFileUpload(self._file_path, resumable=True)
            google_service.files().create(
                body=file_metadata, media_body=media, fields="id").execute()
            return f"GoogleDriveBackup: {self._file_path} успех"
        except ThereIsNoSubPathLikeThatInGoogleDrive:
            return f"GoogleDriveBackup: подпути {dst_path} в " \
                   f"Google Drive не существует"
        except FileNotFoundError:
            return f"GoogleDriveBackup: Файл {self._file_path} не найден"
        except PermissionError:
            return f"GoogleDriveBackup: Ошибка доступа к файлу {self._file_path}"
        except Exception:
            return f"GoogleDriveBackup: неизвестная ошибка " \
                   f"при попытке отправить файл {self._file_path}"

    def restore_from_google_drive(self, google_service, dst_path, **kwargs):
        try:
            restore_result = []
            google_files = GoogleDriveCloud.get_target_files(
                google_service, self._file_path)
            for g_file in google_files:
                try:
                    media = google_service.files().get_media(
                        fileId=g_file["id"])
                    with open(dst_path + g_file["name"], "wb") as file:
                        downloader = MediaIoBaseDownload(file, media)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                    restore_result.append(
                        f"GoogleDriveRestore: восстановление файла "
                        f"{self._file_path} - успех")
                except PermissionError:
                    restore_result.append(
                        f"GoogleDriveRestore: ошибка доступа к файлу " \
                        f"{dst_path + g_file['name']}")
            return "\n".join(restore_result)
        except Exception as ex:
            return f"GoogleDriveRestore: неизвестная ошибка {ex} " \
                   f"при попытке скачать файл {self._file_path}"
    @property
    def restore_title(self):
        return self._file_path

    @property
    def restore_type_description(self):
        return "Файл"

    @property
    def restore_log(self):
        return self._restore_log

    @property
    def backup_title(self):
        return self._file_path

    @property
    def type_description(self):
        return "Файл"

    @property
    def backup_log(self):
        return self._backup_log
