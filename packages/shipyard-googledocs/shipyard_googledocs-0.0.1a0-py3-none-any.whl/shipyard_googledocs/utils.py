import json
import os
import re
from pathlib import Path
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from shipyard_templates import (
    ShipyardLogger,
    standardize_errors,
    CloudStorage,
    ExitCodeException,
)
from shipyard_googledocs import exceptions

logger = ShipyardLogger.get_logger()
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file",
]


def extract_doc_id_from_url(doc_url: str) -> str:
    """
    Extracts the document ID from a full Google Docs URL.
    """
    match = re.search(r"/document/d/([a-zA-Z0-9-_]+)", doc_url)
    if match:
        doc_id = match.group(1)
        logger.info(f"Extracted document ID: {doc_id}")
        return doc_id
    else:
        logger.warning(f"Could not extract document ID from URL: {doc_url}.")
        return None


def is_existing_file_path(string_value: str) -> bool:
    """Checks if the input string is a file path."""
    return Path(string_value).is_file()


def is_json_string(string_value: str) -> bool:
    """Checks if the input string is a JSON string."""
    string_value = string_value.strip()
    try:
        json.loads(string_value)
    except ValueError:
        return False
    return True


@standardize_errors
def get_service():
    """
    Attempts to create the Google Docs and Drive clients using the available credentials.
    """
    logger.info("Creating Google Docs and Drive clients")
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    return service, drive_service


@standardize_errors
def get_credentials():
    """
    Retrieve Google API credentials using one of the following methods, in order of precedence:

    1. If the environment variable `GOOGLE_APPLICATION_CREDENTIALS` is set:
       - If it points to a valid file path, load the service account credentials from the file.
       - Otherwise, attempt to parse the value as raw JSON and load credentials from it.
       - This is intended as a developer override and is not expected to be used in production.

    2. If the environment variable `OAUTH_ACCESS_TOKEN` is set, use it to construct
       an OAuth `Credentials` object.

    If neither environment variable is set, this indicates a misconfigured environment and an error is raised.

    Returns:
        google.auth.credentials.Credentials
    """
    serv_account = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    access_token = os.getenv("OAUTH_ACCESS_TOKEN")
    if access_token:
        logger.info("Using access token for authentication")
        return Credentials(token=access_token, scopes=SCOPES)
    elif serv_account:
        logger.info("Using service account for authentication")
        if os.path.isfile(serv_account):
            logger.info("Detected service account as file path")
            try:
                return service_account.Credentials.from_service_account_file(
                    serv_account, scopes=SCOPES
                )
            except Exception as e:
                raise exceptions.InvalidCredentialsError(
                    f"Failed to load credentials from file: {e}"
                )

        logger.debug("Parsing service account as JSON string")
        try:
            json_creds = json.loads(serv_account)
        except json.JSONDecodeError as e:
            raise exceptions.InvalidFormatError(f"Invalid JSON credentials: {e}")

        try:
            return service_account.Credentials.from_service_account_info(
                json_creds, scopes=SCOPES
            )
        except Exception as e:
            raise exceptions.InvalidCredentialsError(
                f"Failed to load credentials from JSON: {e}"
            )
    else:
        logger.error(
            "No credentials found. Expected either OAUTH_ACCESS_TOKEN or GOOGLE_APPLICATION_CREDENTIALS to be set."
        )
        raise ExitCodeException(
            "Missing credentials and no fallback available.",
            exit_code=CloudStorage.EXIT_CODE_UNKNOWN_ERROR,
        )
