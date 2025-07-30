#!/usr/bin/env python3

import argparse
import os
import socket
import sys
from shipyard_bp_utils import files as shipyard
from shipyard_templates import ShipyardLogger, ExitCodeException, Documents
from shipyard_googledocs import GoogleDocsClient

logger = ShipyardLogger.get_logger()
socket.setdefaulttimeout(600)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-account", dest="service_account", required=False)
    parser.add_argument(
        "--source-file-url",
        dest="file_url",
        required=True,
        help="Full URL to the Google Doc",
    )
    parser.add_argument(
        "--destination-file-name",
        dest="destination_file_name",
        required=True,
        help="Name to save the .txt file locally",
    )
    parser.add_argument(
        "--destination-folder-name",
        dest="destination_folder_name",
        default="downloads",
        help="Optional folder path to save the file",
    )
    return parser.parse_args()


def main():
    try:
        args = get_args()
        doc_url = args.file_url
        full_destination_path = shipyard.combine_folder_and_file_name(
            folder_name=os.path.join(os.getcwd(), args.destination_folder_name),
            file_name=args.destination_file_name,
        )
        os.makedirs(os.path.dirname(full_destination_path), exist_ok=True)

        client = GoogleDocsClient(service_account_credential=args.service_account)
        logger.info("Successfully connected to Google Docs client.")
        full_text = client.fetch(doc_url)

        with open(full_destination_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        file_name = os.path.basename(full_destination_path)
        logger.info(
            f"Saved document: {file_name} to {full_destination_path} with {len(full_text)} characters."
        )

    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(Documents.EXIT_CODE_FILE_NOT_FOUND)

    except ExitCodeException as e:
        logger.error(e)
        sys.exit(e.exit_code)

    except Exception as e:
        logger.error(f"An unexpected error occurred\n{e}")
        sys.exit(Documents.EXIT_CODE_UNKNOWN_ERROR)
    else:
        logger.info(f"Download completed successfully to {full_destination_path}")


if __name__ == "__main__":
    main()
