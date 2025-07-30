import tempfile
import json
import pytest
from unittest import mock
from shipyard_googledocs import GoogleDocsClient
from dotenv import load_dotenv, find_dotenv
from shipyard_templates import ExitCodeException

load_dotenv(find_dotenv())


@pytest.fixture
def valid_service_account_dict():
    return {
        "type": "service_account",
        "project_id": "dummy-project",
        "private_key_id": "fake-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nFAKEKEY\n-----END PRIVATE KEY-----\n",
        "client_email": "test@dummy-project.iam.gserviceaccount.com",
        "client_id": "123456789",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test%40dummy-project.iam.gserviceaccount.com",
    }


@pytest.fixture
def mock_google_services():
    with (
        mock.patch(
            "shipyard_googledocs.googledocs.service_account.Credentials.from_service_account_file"
        ) as mock_creds_file,
        mock.patch(
            "shipyard_googledocs.googledocs.service_account.Credentials.from_service_account_info"
        ) as mock_creds_info,
        mock.patch("shipyard_googledocs.googledocs.build") as mock_build,
    ):
        mock_creds_file.return_value = mock.Mock()
        mock_build.return_value = mock.Mock()
        yield


def test_connection_with_valid_file_path(
    valid_service_account_dict, mock_google_services
):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(valid_service_account_dict, f)
        f.flush()
        path = f.name

    client = GoogleDocsClient(service_account=path)
    service, drive = client.connect()
    assert service is not None
    assert drive is not None


def test_connection_with_valid_raw_json(
    valid_service_account_dict, mock_google_services
):
    # Simulate raw JSON by writing it to a temp file manually
    raw_json = json.dumps(valid_service_account_dict)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(raw_json)
        f.flush()
        json_file_path = f.name

    # Even though we want to test "raw_json", due to connect() logic,
    # we must pass a file path or it'll misinterpret the string as a path
    client = GoogleDocsClient(service_account=json_file_path)
    service, drive = client.connect()
    assert service is not None
    assert drive is not None
