# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "shipyard-googlesheets",
#     "shipyard-templates>=0.9.0"
# ]
# ///
import os
import sys

from shipyard_templates import ShipyardLogger

from shipyard_googlesheets import GoogleSheetsClient

logger = ShipyardLogger.get_logger()


def main():
    sys.exit(GoogleSheetsClient(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]).connect())


if __name__ == "__main__":
    main()
