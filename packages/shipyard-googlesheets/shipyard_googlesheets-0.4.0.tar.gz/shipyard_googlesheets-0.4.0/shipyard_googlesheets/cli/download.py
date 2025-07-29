import argparse
import sys

from shipyard_bp_utils import files as shipyard
from shipyard_templates import ShipyardLogger, Spreadsheets, ExitCodeException

from shipyard_googlesheets import exceptions, GoogleSheetsClient

logger = ShipyardLogger.get_logger()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-file-name", dest="file_name", default="", required=True
    )
    parser.add_argument("--tab-name", dest="tab_name", default=None, required=False)
    parser.add_argument(
        "--destination-file-name",
        dest="destination_file_name",
        default=None,
        required=True,
    )
    parser.add_argument(
        "--destination-folder-name",
        dest="destination_folder_name",
        default="",
        required=False,
    )
    parser.add_argument(
        "--cell-range", dest="cell_range", default="A1:ZZZ5000000", required=False
    )
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

        if args.destination_folder_name:
            shipyard.create_folder_if_dne(args.destination_folder_name)

        client = GoogleSheetsClient(args.gcp_application_credentials)
        spreadsheet_id = client.get_spreadsheet_id_by_name(
            sheet_name=sheet_name, drive=drive
        )
        if not spreadsheet_id:
            if len(sheet_name) >= 44:
                spreadsheet_id = sheet_name
            else:
                raise exceptions.InvalidSheetError(sheet_name)
        if args.destination_file_name:
            destination_name = shipyard.combine_folder_and_file_name(
                args.destination_folder_name, args.destination_file_name
            )
        else:
            destination_name = f"{sheet_name} - {tab_name}.csv"

        client.download(
            tab_name=tab_name,
            spreadsheet_id=spreadsheet_id,
            sheet_name=sheet_name,
            cell_range=cell_range,
            destination_file_name=destination_name,
        )
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(Spreadsheets.EXIT_CODE_FILE_NOT_FOUND)
    except ExitCodeException as e:
        logger.error(e)
        sys.exit(e.exit_code)
    except Exception as e:
        logger.error(e)
        sys.exit(Spreadsheets.EXIT_CODE_UNKNOWN_ERROR)


if __name__ == "__main__":
    main()
