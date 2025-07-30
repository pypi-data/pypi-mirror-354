# /// script
# requires-python = ">=3.1"
# dependencies = [
#     "shipyard_googledocs",
#     "shipyard-templates>=0.9.0"
# ]
# ///
import os
import sys

from shipyard_templates import ShipyardLogger

from shipyard_googledocs import GoogleDocsClient

logger = ShipyardLogger.get_logger()


def main():
    try:
        credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        credentials = credentials.replace("\n", "\\n")

        GoogleDocsClient(service_account=credentials).connect()
        logger.authtest("Successfully connected to google sheets")
        sys.exit(0)
    except Exception as e:
        logger.authtest(
            f"Could not connect to Google Sheets with the Service Account provided due to {e}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
