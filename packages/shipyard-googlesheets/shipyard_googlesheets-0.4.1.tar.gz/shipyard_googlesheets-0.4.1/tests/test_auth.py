import os
from shipyard_googlesheets import GoogleSheetsClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def test_good_connection():
    client = GoogleSheetsClient(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    exit_code = client.connect()

    assert exit_code == 0


def test_bad_connection():
    client = GoogleSheetsClient("{creds:bad_credentials}")
    exit_code = client.connect()

    assert exit_code == 1
