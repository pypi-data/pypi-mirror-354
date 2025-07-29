import argparse

import socket
import sys

from shipyard_templates import ShipyardLogger, ExitCodeException, Spreadsheets
from shipyard_googlesheets import exceptions, GoogleSheetsClient


logger = ShipyardLogger.get_logger()

socket.setdefaulttimeout(600)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--destination-file-name", dest="file_name", default="", required=False
    )
    parser.add_argument(
        "--cell-range", dest="cell_range", default="A1:ZZZ5000000", required=False
    )
    parser.add_argument("--tab-name", dest="tab_name", default=None, required=False)
    parser.add_argument(
        "--service-account",
        dest="gcp_application_credentials",
        default=None,
        required=False,
    )
    parser.add_argument("--drive", dest="drive", default=None, required=False)
    return parser.parse_args()


def main():
    try:
        args = get_args()
        sheet_name = args.file_name
        tab_name = args.tab_name
        cell_range = args.cell_range or "A1:ZZZ5000000"
        drive = args.drive

        client = GoogleSheetsClient(args.gcp_application_credentials)

        spreadsheet_id = client.get_spreadsheet_id_by_name(
            sheet_name=sheet_name, drive=drive
        )
        if not spreadsheet_id:
            if len(sheet_name) >= 44:
                spreadsheet_id = sheet_name
            else:
                raise exceptions.InvalidSheetError(sheet_name)

        # check if workbook exists in the spreadsheet
        client.clear_sheet(
            sheet_name=sheet_name,
            spreadsheet_id=spreadsheet_id,
            tab_name=tab_name,
            cell_range=cell_range,
        )
    except ExitCodeException as e:
        logger.error(e)
        sys.exit(e.exit_code)
    except Exception as e:
        logger.error(e)
        sys.exit(Spreadsheets.EXIT_CODE_UNKNOWN_ERROR)


if __name__ == "__main__":
    main()
