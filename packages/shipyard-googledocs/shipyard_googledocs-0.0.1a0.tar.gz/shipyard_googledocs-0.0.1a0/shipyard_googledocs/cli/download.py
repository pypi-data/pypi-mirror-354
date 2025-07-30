#!/usr/bin/env python3
import argparse
import os
import socket
import sys
from shipyard_bp_utils import files as shipyard
from shipyard_templates import ShipyardLogger, ExitCodeException, Docs
from shipyard_googledocs import utils, exceptions

logger = ShipyardLogger.get_logger()
socket.setdefaulttimeout(600)


def get_args():
    parser = argparse.ArgumentParser()
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


def download_google_docs_file(
    docs_service,
    doc_url,
    destination_path,
):
    """
    Downloads a Google Doc's contents and saves them as plain text.
    """
    doc_id = utils.extract_doc_id_from_url(doc_url)
    if not doc_id:
        raise exceptions.InvalidDocUrlError(doc_url)
    try:
        doc = docs_service.documents().get(documentId=doc_id).execute()
        content = []

        for element in doc.get("body", {}).get("content", []):
            paragraph = element.get("paragraph")
            if paragraph:
                text = "".join(
                    run.get("textRun", {}).get("content", "")
                    for run in paragraph.get("elements", [])
                )
                content.append(text)

        full_text = "\n".join(content)
        if not full_text.strip():
            logger.error(f"Google Doc '{doc_id}' is empty. Nothing to download.")
            raise exceptions.DownloadError(doc_id, err_msg="doc is empty")
        with open(destination_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        file_name = os.path.basename(destination_path)
        logger.info(f"Saving to {destination_path}")
        logger.info(
            f"Successfully downloaded Google Doc '{doc_id}' → '{file_name}'  with {len(full_text)} characters"
        )
    except Exception as e:
        logger.error(
            f"Failed to download content from Doc '{doc_id}' (ID {doc_id}): {e}"
        )
        raise exceptions.DownloadError(doc_id, err_msg=str(e))


def main():
    try:
        args = get_args()
        docs_service, drive_service = utils.get_service()
        doc_url = args.file_url
        full_destination_path = shipyard.combine_folder_and_file_name(
            folder_name=os.path.join(os.getcwd(), args.destination_folder_name),
            file_name=args.destination_file_name,
        )
        os.makedirs(os.path.dirname(full_destination_path), exist_ok=True)
        download_google_docs_file(
            docs_service=docs_service,
            doc_url=doc_url,
            destination_path=full_destination_path,
        )

    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(Docs.EXIT_CODE_FILE_NOT_FOUND)

    except ExitCodeException as e:
        logger.error(e)
        sys.exit(e.exit_code)

    except Exception as e:
        logger.error(f"An unexpected error occurred\n{e}")
        sys.exit(Docs.EXIT_CODE_UNKNOWN_ERROR)


if __name__ == "__main__":
    main()
