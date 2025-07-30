import os
import tempfile
from shipyard_googledocs.utils import is_existing_file_path, is_json_string

from google.oauth2 import service_account
from googleapiclient.discovery import build
from shipyard_templates import Docs, ExitCodeException


class GoogleDocsClient(Docs):
    def __init__(self, service_account: str) -> None:
        """
        Initialize the Google Docs client. Using either a file path or a JSON string for the service account.
        Args:
            service_account: The service account credentials. This can be a file path or a JSON string.
        """
        self.service_account = service_account

    def _set_env_vars(self):
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "w") as tmp:
            tmp.write(self.service_account)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
        return path

    def connect(self):
        if is_existing_file_path(self.service_account):
            path = self.service_account
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.service_account
        elif is_json_string(self.service_account):
            path = self._set_env_vars()
        else:
            raise ExitCodeException(
                "Invalid service account credentials. Please provide a valid file path or JSON string.",
                self.EXIT_CODE_INVALID_TOKEN,
            )

        creds = service_account.Credentials.from_service_account_file(path)
        service = build("docs", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)

        return service, drive_service

    def fetch(self):
        pass

    def upload(self):
        pass
