import json
import tempfile
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from shipyard_templates import CloudStorage, ExitCodeException
from typing import Optional, Union, List, Any
from googleapiclient.http import MediaIoBaseDownload
from functools import cached_property
from google.auth import load_credentials_from_file
import re


from shipyard_templates import ShipyardLogger

logger = ShipyardLogger.get_logger()


class GoogleDriveClient(CloudStorage):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    EXIT_CODE_DRIVE_ACCESS_ERROR = 209

    def __init__(
        self,
        service_account_credential: str,
        shared_drive_name: Optional[str] = None,
    ) -> None:
        self.service_account_credential = service_account_credential
        self.shared_drive_name = shared_drive_name
        self.drive_id = None
        self.folder_id = None
        self.folder_name = None

    @cached_property
    def credentials(self):
        credential_file_path, temp_path = None, None
        try:
            json.loads(self.service_account_credential)

            fd, temp_path = tempfile.mkstemp(suffix=".json")
            logger.info(f"Storing JSON credentials temporarily at {temp_path}")
            with os.fdopen(fd, "w") as tmp:
                tmp.write(self.service_account_credential)
            credential_file_path = temp_path

            logger.debug("Loaded Credentials from JSON string via temporary file.")

        except (ValueError, TypeError) as e:
            logger.debug(
                f"Failed to parse service_account_credential as JSON: {e}. "
                "Assuming it is a file path."
            )
            if not os.path.exists(self.service_account_credential):
                raise ExitCodeException(
                    f"Provided service_account_credential is neither valid JSON "
                    f"nor a readable file",
                    CloudStorage.EXIT_CODE_INVALID_CREDENTIALS,
                )
            else:
                credential_file_path = self.service_account_credential

        creds, _ = load_credentials_from_file(credential_file_path, scopes=self.SCOPES)
        logger.debug(f"Loaded Credentials from file at: {credential_file_path}")
        if temp_path:
            os.remove(temp_path)
            logger.debug(f"Deleted temporary credentials file {temp_path}")

        return creds

    @cached_property
    def service(self):
        """
        Read‐only property returning the Google Drive API client.
        """
        try:
            return build("drive", "v3", credentials=self.credentials)
        except Exception as e:
            logger.debug(f"Failed to build Drive service: {e}")
            raise

    def connect(self):
        """
        Simple connectivity test: attempts to access both clients.
        Returns 0 on success, 1 on failure (logging the error).
        """
        try:
            _ = self.service
            return 0
        except Exception as e:
            logger.authtest(f"Failed to connect to Drive API. Response: {e}")
            return 1

    def upload(
            self,
            file_path: str,
            drive_folder: Optional[str] = None,
            drive_file_name: Optional[str] = None,
            drive: Optional[str] = None,
    ):
        """Uploads a file to a shared Google Drive

        Args:
            file_path: The path of the file to load
            drive_file_name: The name that the uploaded file in drive will have
            drive_folder: The ID of the folder in Google drive
            drive: The name or ID of the shared drive
        """

        # NOTE: check to see that the folder is shared with the service account
        if drive:
            self.shared_drive_name = drive
            self.drive_id = self.get_drive_id(
                drive_id=self.shared_drive_name
            )
            # if the drive is provided, but not found, then the service account doesn't have access and needs it to be shared
            if not self.drive_id:
                raise ExitCodeException(
                    f"Service Account does not have access to the following drive: {self.shared_drive_name}. Please visit the authorization guide to see how to share the Drive to the service account",
                    self.EXIT_CODE_DRIVE_ACCESS_ERROR,
                )

        try:
            if drive_folder:
                self.folder_name = drive_folder
                self.folder_id = self.get_folder_id(
                    folder_identifier=self.folder_name,
                    drive_id=self.drive_id,
                )
                if not self.folder_id and not self.is_folder_id(
                        self.folder_name
                ):
                    folder_results = self.create_remote_folder(
                        folder_name=self.folder_name,
                        drive_id=self.drive_id,
                    )
                    self.folder_id = folder_results

            # use the base name of the file if not provided
            if not drive_file_name:
                drive_file_name = os.path.basename(file_path)
            file_metadata = {"name": drive_file_name, "parents": []}
            # if the folder exists, check to see if it has been shared with the drive correctly, if not then throw exception
            if self.folder_id:
                # FIXME: This throws an exception every time, needs to be fixed
                # if drive_utils.is_folder_shared(
                #     service_account_email=self.email,
                #     folder_id=self.folder_id,
                #     drive_service=self.service,
                # ):
                file_metadata["parents"].append(self.folder_id)
            elif self.drive_id:
                self.folder_id = self.drive_id
                file_metadata["parents"].append(self.folder_id)
            else:
                self.folder_id = "root"
                file_metadata["parents"].append(self.folder_id)

            # check to see if the file exists or not
            update = False
            if self.does_file_exist(
                    parent_folder_id=self.folder_id,
                    file_name=drive_file_name,
                    drive_id=self.drive_id,
            ):
                parents = file_metadata.pop("parents")
                update = True
                if parents != []:
                    self.folder_id = parents[0]  # update the folder ID

            media = MediaFileUpload(file_path, resumable=True)
            if update:
                file_id = self.get_file_id(
                    file_name=drive_file_name,

                    drive_id=self.drive_id,
                    folder_id=self.folder_id,  # NOTE: This was added after tests. Need to retest
                )
                upload_file = (
                    self.service.files()
                    .update(
                        fileId=file_id,
                        body=file_metadata,
                        media_body=media,
                        supportsAllDrives=True,
                        fields=("id"),
                        addParents=self.folder_id,
                    )
                    .execute()
                )
                logger.info(f"Updated file {file_id}")

            else:
                upload_file = (
                    self.service.files()
                    .create(
                        body=file_metadata,
                        media_body=media,
                        fields=("id"),
                        supportsAllDrives=True,
                    )
                    .execute()
                )
                logger.info(f"Newly created file is {upload_file.get('id')}")
        except FileNotFoundError as fe:
            raise ExitCodeException(
                message=str(fe), exit_code=self.EXIT_CODE_FILE_NOT_FOUND
            )
        except ExitCodeException as ec:
            raise ExitCodeException(message=ec.message, exit_code=ec.exit_code)
        except Exception as e:
            raise ExitCodeException(
                message=f"Error in uploading file to google drive: {str(e)}",
                exit_code=self.EXIT_CODE_UPLOAD_ERROR,
            )

    def move(self):
        pass

    def remove(self):
        pass

    def download(
        self,
        file_id: str,
        drive_file_name: str,
        drive_folder: Optional[str] = None,
        drive: Optional[str] = None,
        destination_file_name: Optional[str] = None,
    ):
        """Downloads a file from Google Drive locally

        Args:
            file_id: The ID of the file to download
            drive_file_name: The name of the file to download
            drive_folder: The optional name of the folder or the ID of folder. If not provided, then it will look for the file within the root directory of the drive
            drive: The optional name or ID of the shared drive
            destination_file_name: The optional name of the downloaded file to have. If not provided, then the file will have the same name as it did in Google Drive
        """
        if drive:
            self.drive_id = self.get_drive_id(drive_id=drive)

        if drive_folder:
            try:
                self.folder_id = self.get_folder_id(
                    folder_identifier=drive_folder,
                    drive_id=self.drive_id,
                )
            except ExitCodeException as ec:
                raise ExitCodeException(ec.message, ec.exit_code)

        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = open(destination_file_name, "wb")
            downloader = MediaIoBaseDownload(fh, request)
            complete = False
            while not complete:
                status, complete = downloader.next_chunk()
        except Exception as e:
            raise ExitCodeException(
                message=str(e), exit_code=self.EXIT_CODE_DOWNLOAD_ERROR
            )
        else:
            return

    def get_all_folder_ids(self, drive_id: Optional[str] = None) -> List[Any]:
        # Set the query to retrieve all folders
        query = "mimeType='application/vnd.google-apps.folder' and trashed=false"

        # Execute the query to get the list of folders
        if drive_id:
            folders = self.list_files(query, drive_id=drive_id)
        else:
            folders = self.list_files(query)
        # Extract and return the folder IDs
        folder_ids = [folder["id"] for folder in folders]
        # folder_ids.append('root') # add so that the files not within a folder will be returned as well
        return folder_ids

    def get_file_matches(
        self,
        pattern: str,
        folder_id: Optional[str] = None,
        drive_id: Optional[str] = None,
    ) -> List[Any]:
        """Helper function to return all the files that match a particular pattern

        Args:
            pattern: The pattern to search for
            folder_id: The folder to search within. If omitted, all file matches across all folders will be returned
            drive_id: The shared drive to search within

        Raises:
            ExitCodeException:

        Returns: The list of the matches

        """
        try:
            files = []
            if folder_id:
                query = f"'{folder_id}' in parents"
                if drive_id:
                    files = self.list_files(query, drive_id=drive_id)
                else:
                    files = self.list_files(query)

            else:
                all_folder_ids = self.get_all_folder_ids(drive_id=drive_id)
                for f_id in all_folder_ids:
                    query = f"'{f_id}' in parents"
                    if drive_id:
                        files.extend(self.list_files(query, drive_id=drive_id))
                    else:
                        files.extend(self.list_files(query))

                # grab the files in the root
                root_query = (
                    "trashed=false and mimeType!='application/vnd.google-apps.folder'"
                )
                if drive_id:
                    root_results = self.list_files(root_query, drive_id=drive_id)
                else:
                    root_results = self.list_files(root_query)
                files.extend(root_results)

            matches = []
            id_set = set()
            for f in files:
                if re.search(pattern, f["name"]) and f["id"] not in id_set:
                    matches.append(f)
                    id_set.add(f["id"])
        except Exception as e:
            raise ExitCodeException(f"Error in finding matching files: {str(e)}", 210)

        else:
            return matches

    def get_drive_id(self, drive_id: str) -> Union[str, None]:
        """Helper function to grab the drive ID when either the name of the drive or the ID is provided. This is instituted for backwards compatibility in the Shipyard blueprint

        Args:
            drive_id:  The name of the drive or the ID from the URL

        Returns: The ID of the drive or None if not found

        """
        try:
            if len(drive_id) == 19 and str(drive_id).startswith("0A"):
                return drive_id
            else:
                results = (
                    self.service.drives()
                    .list(q=f"name = '{drive_id}'", fields="drives(id)")
                    .execute()
                )
                drives = results.get("drives", [])
                if drives:
                    return drives[0]["id"]
                else:
                    return None
        except Exception:
            return None

    def get_folder_id(
        self,
        folder_identifier: Optional[str] = None,
        drive_id: Optional[str] = None,
    ) -> Union[str, None]:
        """Helper function to grab the folder ID when provided either the name of the folder or the ID (preferred). This is instituted for backwards compatibility in the Shipyard blueprint

        Args:
            drive_id: The optional ID of the shared drive to search within
            folder_identifier: The name of the folder or the ID from the URL

        Returns: The folder ID or None if nonexistent

        """
        if not folder_identifier:
            return None
        try:
            # every folder ID starts with 1 and is 33 chars long
            if self.is_folder_id(folder_identifier):
                return folder_identifier
            else:
                folder_names = folder_identifier.split("/")
                tmp_id = "root"  # this will be iteratively updated
                for folder_name in folder_names:
                    if tmp_id == "root":
                        query = f"trashed=false and mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
                    else:
                        query = f"'{tmp_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
                    if not drive_id:
                        folders = self.list_files(query)
                    else:
                        folders = self.list_files(query, drive_id=drive_id)
                    if len(folders) > 1:
                        raise ExitCodeException(
                            f"Multiple folders with name {folder_identifier} found, please use the folder ID instead",
                            204,
                        )
                    if folders:
                        tmp_id = folders[0]["id"]
                    else:
                        return None
                return tmp_id

        except ExitCodeException as ec:
            raise ExitCodeException(ec.message, ec.exit_code)
        except Exception:
            return None

    def create_remote_folder(
        self,
        folder_name: str,
        parent_id: Optional[str] = None,
        drive_id: Optional[str] = None,
    ) -> str:
        """Helper function to create a folder in Google Drive

        Args:
            folder_name: The name of the folder to create
            parent_id: The optional folder to place the newly created folder within
            drive_id: The optional drive to create the folder in

        Raises:
            ExitCodeException:

        Returns: The ID of the newly created folder

        """
        body = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_id:
            body["parents"] = [parent_id]
        if drive_id and not parent_id:
            body["parents"] = [drive_id]

        try:
            folder = (
                self.service.files()
                .create(body=body, supportsAllDrives=True, fields=("id"))
                .execute()
            )
        except Exception as e:
            raise ExitCodeException(
                f"Failed to create folder {folder_name} in Goolge Drive", 208
            )
        return folder["id"]

    def get_file_id(
        self,
        file_name: str,
        drive_id: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> Union[str, None]:
        """Helper function to retrieve the file id in Google Drive

        Args:
            file_name: The name of the file to lookup in Google Drive
            drive_id: The Optional ID of the drive
            folder_id: The optional ID of the folder. This is only necessary if the file resides in a folder

        Raises:
            ExitCodeException:

        Returns: The ID of the file if exists, otherwise None

        """
        query = f"name='{file_name}'"
        if folder_id:
            query += f"and '{folder_id}' in parents"
        try:
            if drive_id:
                results = self.list_files(query, drive_id=drive_id)
            else:
                results = self.list_files(query)

        except Exception as e:
            raise ExitCodeException(
                f"Error in fetching file id: {str(e)}", exit_code=203
            )

        return results[0]["id"] if results else None

    def is_folder_shared(self, service_account_email: str, folder_id: str) -> bool:
        """Helper function to see if a provided folder is shared with the service account

        Args:

            service_account_email: The email of the service account
            folder_id: The ID of the folder in Google Drive

        Returns: True if folder is shared, False if not
        """
        try:
            permissions = self.service.permissions().list(fileId=folder_id).execute()
            for permission in permissions.get("permissions", []):
                if (
                    permission["type"] == "user"
                    and permission["emailAddress"] == service_account_email
                ):
                    return True

        except Exception as e:
            logger.warning(
                f"An exception was found during this call most likely indicating that no folder ID exists, returning False. Exception message: {str(e)}"
            )
            return False

        else:
            logger.warning("Folder ID is not shared with service account")
            return False

    def does_file_exist(
        self,
        parent_folder_id: str,
        file_name: str,
        drive_id: Optional[str] = None,
    ) -> bool:
        """Helper function to see if the file already exists in the accessible Google Drive

        Args:
            parent_folder_id: The ID of the parent folder
            file_name: The name of the file
            drive_id: The optional ID of the shared drive

        Returns: True if exists, False if not

        """
        query = f"'{parent_folder_id}' in parents and name='{file_name}'"
        try:
            if drive_id:
                results = self.list_files(query, drive_id=drive_id)
            else:
                results = self.list_files(query)
            return bool(results)
        except Exception as e:
            # this means that the file was not found
            logger.warning(
                f"An exception was thrown and now file was found, returning False: {str(e)}"
            )
            return False

    @staticmethod
    def is_folder_id(folder_identifier: str) -> bool:
        """Helper function to determine if the input is a legitimate folder ID or a folder name

        Args:
            folder_identifier: Either the folder name or the ID from the URL

        Returns: True if the format matches that of a folder ID, false otherwise

        """
        if len(folder_identifier) == 33 and str(folder_identifier).startswith("1"):
            return True
        return False

    def list_files(
        self,
        query,
        drive_id: Optional[str] = None,
    ) -> List[Any]:
        """List files in Google Drive based on a query.

        Args:
            query: The query to filter files.
            drive_id: The optional ID of the shared drive.

        Returns:
            A list of files matching the query.
        """

        if drive_id:
            results = (
                self.service.files()
                .list(
                    q=query,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    corpora="drive",
                    driveId=drive_id,
                    fields=("id"),
                )
                .execute()
            )
        else:
            results = self.service.files().list(q=query).execute()
        return results.get("files", [])
