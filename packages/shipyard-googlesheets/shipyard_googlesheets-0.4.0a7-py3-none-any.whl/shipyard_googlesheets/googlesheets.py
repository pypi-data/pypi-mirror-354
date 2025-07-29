import csv
import json
import os
import socket
import tempfile

from functools import cached_property
from googleapiclient.discovery import build

from shipyard_templates import Spreadsheets, ShipyardLogger, ExitCodeException
from shipyard_googlesheets import exceptions
from google.auth import load_credentials_from_file

logger = ShipyardLogger.get_logger()
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
socket.setdefaulttimeout(600)


class GoogleSheetsClient(Spreadsheets):
    def __init__(self, service_account_credential):
        """
        Initializes the Google Sheets Client with the provided service account.
        The `service_account_credential` argument may be:
          - a JSON string containing the service account key, or
          - a file path to a JSON key file.
        """
        if not service_account_credential:
            raise ExitCodeException(
                "Service account is required to initialize Google Sheets Client.",
                Spreadsheets.EXIT_CODE_INVALID_TOKEN,
            )
        self.service_account_credential = service_account_credential

    @cached_property
    def credentials(self):
        credential_file_path, temp_path = None, None
        try:
            info = json.loads(self.service_account_credential)
            if isinstance(info, dict):
                fd, temp_path = tempfile.mkstemp(suffix=".json")
                logger.info(f"Storing JSON credentials temporarily at {temp_path}")
                with os.fdopen(fd, "w") as tmp:
                    tmp.write(self.service_account_credential)
                credential_file_path = temp_path

                logger.debug("Loaded Credentials from JSON string via temporary file.")

        except (ValueError, TypeError):
            if not os.path.exists(self.service_account_credential):
                raise ExitCodeException(
                    f"Provided service_account_credential is neither valid JSON "
                    f"nor a readable file: {self.service_account_credential}",
                    Spreadsheets.EXIT_CODE_INVALID_TOKEN,
                )
            else:
                credential_file_path = self.service_account_credential

        creds, _ = load_credentials_from_file(credential_file_path, scopes=SCOPES)
        logger.debug(f"Loaded Credentials from file at: {credential_file_path}")
        if temp_path:
            os.remove(temp_path)
            logger.debug(f"Deleted temporary credentials file {temp_path}")

        return creds

    @cached_property
    def service(self):
        """
        Read‐only property returning the Google Sheets API client.
        """
        try:
            return build("sheets", "v4", credentials=self.credentials)
        except Exception as e:
            logger.debug(f"Failed to build Sheets service: {e}")
            raise

    @cached_property
    def drive_service(self):
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
            _ = self.drive_service
            return 0
        except Exception:
            logger.authtest(
                f"Failed to connect to Google Sheets or Drive API. "
                f"Ensure your credentials is a valid JSON string or file path"
            )
            return 1

    def fetch(self, tab_name, spreadsheet_id, cell_range):
        if tab_name:
            if self.check_workbook_exists(
                spreadsheet_id=spreadsheet_id, tab_name=tab_name
            ):
                cell_range = f"{tab_name}!{cell_range}"
            else:
                raise exceptions.TabNotFoundError(tab_name)

        sheet = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=cell_range)
            .execute()
        )
        return sheet

    def upload(
        self,
        sheet_name,
        source_full_path,
        starting_cell,
        spreadsheet_id,
        tab_name,
    ):
        """
        Uploads a single CSV file to Google Sheets. If `spreadsheet_id` is None/empty,
        creates a new spreadsheet named `sheet_name`.

        Returns the Sheets API response.
        """
        try:
            if not spreadsheet_id:
                file_metadata = {
                    "properties": {"title": sheet_name},
                    "namedRanges": {"range": starting_cell},
                }
                spreadsheet = (
                    self.service.spreadsheets()
                    .create(body=file_metadata, fields="spreadsheetId")
                    .execute()
                )
                spreadsheet_id = spreadsheet["spreadsheetId"]

            workbook_exists = self.check_workbook_exists(
                spreadsheet_id=spreadsheet_id, tab_name=tab_name
            )
            if not workbook_exists:
                self.add_workbook(spreadsheet_id=spreadsheet_id, tab_name=tab_name)

            data = []
            with open(source_full_path, encoding="utf-8", newline="") as f:
                reader = csv.reader(
                    (line.replace("\0", "") for line in f), delimiter=","
                )
                data.extend(row for row in reader if set(row) != {""})

            _range = f"{starting_cell}:ZZZ5000000" if starting_cell else "A1:ZZZ5000000"
            if tab_name:
                _range = f"{tab_name}!{_range}"

            body = {
                "value_input_option": "RAW",
                "data": [
                    {
                        "range": _range,
                        "majorDimension": "ROWS",
                        "values": data,
                    }
                ],
            }
            response = (
                self.service.spreadsheets()
                .values()
                .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
                .execute()
            )

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                logger.error(f"File {source_full_path} does not exist.")
            elif hasattr(e, "content"):
                try:
                    err_msg = json.loads(e.content)
                    if "workbook above the limit" in err_msg.get("error", {}).get(
                        "message", ""
                    ):
                        logger.error(
                            f"Failed to upload due to input CSV size {source_full_path} "
                            "(limit is 5,000,000 cells)."
                        )
                except Exception:
                    logger.error("Received an error from Google API: %s", e.content)
            else:
                logger.error(
                    f"Failed to upload spreadsheet {source_full_path} to {sheet_name}: {e}"
                )
            raise

        logger.info(
            f"{source_full_path} successfully uploaded to {sheet_name} (ID: {spreadsheet_id})"
        )
        return response

    def check_workbook_exists(self, spreadsheet_id, tab_name):
        """
        Checks if the tab (worksheet) named `tab_name` exists in the spreadsheet.
        Returns True/False.
        """
        logger.debug(
            f"Checking if workbook/tab '{tab_name}' exists in spreadsheet {spreadsheet_id}"
        )
        try:
            spreadsheet = (
                self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            )
            sheets = spreadsheet.get("sheets", [])
            for sheet in sheets:
                if sheet.get("properties", {}).get("title") == tab_name:
                    return True
            return False
        except Exception as e:
            logger.error(
                f"Failed to check existence of tab '{tab_name}' in spreadsheet '{spreadsheet_id}': {e}"
            )
            raise

    def get_spreadsheet_id_by_name(self, sheet_name, drive=None):
        """
        Attempts to get a spreadsheet ID from Google Drive by filename.
        If `drive` (shared‐drive name) is supplied, searches that Shared Drive;
        otherwise searches "My Drive".
        """
        logger.debug(f"Fetching spreadsheet ID for '{sheet_name}' (drive={drive})")
        try:
            query = 'mimeType="application/vnd.google-apps.spreadsheet"'
            query += f' and name = "{sheet_name}"'

            if drive:
                drive_id = self.get_shared_drive_id(drive)
                logger.debug(f"Searching for '{sheet_name}' in shared drive '{drive}'.")
                results = (
                    self.drive_service.files()
                    .list(
                        q=query,
                        supportsAllDrives=True,
                        includeItemsFromAllDrives=True,
                        corpora="drive",
                        driveId=drive_id,
                        fields="files(id, name)",
                    )
                    .execute()
                )
            else:
                logger.debug(f"Searching for '{sheet_name}' in personal drive.")
                results = (
                    self.drive_service.files()
                    .list(q=query, fields="files(id, name)")
                    .execute()
                )

            files = results.get("files", [])
            for _file in files:
                return _file["id"]
            return None

        except Exception as e:
            logger.error(f"Failed to fetch spreadsheet ID for '{sheet_name}': {e}")
            raise

    def add_workbook(self, spreadsheet_id, tab_name):
        """
        Adds a new tab (worksheet) named `tab_name` to the spreadsheet.
        """
        logger.debug(
            f"Adding workbook/tab '{tab_name}' to spreadsheet {spreadsheet_id}"
        )
        try:
            request_body = {
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": tab_name,
                            }
                        }
                    }
                ]
            }
            return (
                self.service.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
                .execute()
            )
        except Exception as e:
            raise exceptions.WorkbookAddException(e) from e

    def get_shared_drive_id(self, drive):
        """
        Returns the Drive ID for a Shared Drive named `drive`.
        """
        logger.debug(f"Searching for shared drive named '{drive}'")
        try:
            response = self.drive_service.drives().list().execute()
            for _drive in response.get("drives", []):
                if _drive.get("name") == drive:
                    return _drive.get("id")
            return None
        except Exception as e:
            logger.error(f"Failed to list shared drives or find '{drive}': {e}")
            raise

    def download(
        self,
        spreadsheet_id,
        sheet_name,
        tab_name,
        cell_range,
        destination_file_name,
    ):
        """
        Download th contents of a spreadsheet from Google Sheets to local storage in
        the current working directory.
        """

        try:
            sheet = self.fetch(
                tab_name=tab_name,
                spreadsheet_id=spreadsheet_id,
                cell_range=cell_range,
            )
            if not sheet.get("values"):
                logger.warning(f"No values for {sheet_name}.. Not downloading")
                raise exceptions.DownloadError(sheet_name)

            values = sheet["values"]
            with open(destination_file_name, "+w") as f:
                writer = csv.writer(f)
                writer.writerows(values)
            logger.info(
                f"Successfully downloaded {sheet_name} - {tab_name} to {destination_file_name}"
            )
        except Exception as e:
            logger.error(f"Failed to download {sheet_name} from Google Sheets")
            raise e

    def clear_sheet(self, sheet_name, cell_range, spreadsheet_id, tab_name):
        """
        Clears data from a single Google Sheet.
        """
        try:
            if not spreadsheet_id:
                file_metadata = {
                    "properties": {"title": sheet_name},
                    "namedRanges": {"range": cell_range},
                }
                spreadsheet = (
                    self.service.spreadsheets()
                    .create(body=file_metadata, fields="spreadsheetId")
                    .execute()
                )
                spreadsheet_id = spreadsheet["spreadsheetId"]

            if tab_name:
                cell_range = f"{tab_name}!{cell_range}"

            response = (
                self.service.spreadsheets()
                .values()
                .clear(spreadsheetId=spreadsheet_id, range=cell_range)
                .execute()
            )
            logger.info(
                f"{sheet_name} successfully cleared between range {cell_range}."
            )
            return response
        except Exception as e:
            if hasattr(e, "content"):
                err_msg = json.loads(e.content)
                logger.error(
                    f"Failed to clear spreadsheet. Response from Google {sheet_name}: {err_msg}"
                )
            else:
                logger.error(f"Failed to clear spreadsheet {sheet_name}")
            raise e
