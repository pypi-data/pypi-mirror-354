import json
import pytest
from unittest import mock
from shipyard_googledocs import utils
from shipyard_templates import CloudStorage, ExitCodeException
from shipyard_templates import Docs


def test_extract_doc_id_from_valid_url():
    url = (
        "https://docs.google.com/document/d/1AbCDeFGHIJKlmNOPQRSTuvwxyZ1234567890/edit"
    )
    result = utils.extract_doc_id_from_url(url)
    assert result == "1AbCDeFGHIJKlmNOPQRSTuvwxyZ1234567890"


def test_extract_doc_id_from_invalid_url():
    url = "https://docs.google.com/spreadsheets/d/1abcd123"
    result = utils.extract_doc_id_from_url(url)
    assert result is None


@mock.patch("shipyard_googledocs.utils.build")
@mock.patch("shipyard_googledocs.utils.get_credentials")
def test_get_service(mock_get_credentials, mock_build):
    mock_creds = mock.Mock()
    mock_get_credentials.return_value = mock_creds
    mock_build.return_value = mock.Mock()

    service, drive_service = utils.get_service()
    assert service is not None
    assert drive_service is not None


def test_get_credentials_with_access_token(monkeypatch):
    monkeypatch.setenv("OAUTH_ACCESS_TOKEN", "fake-token")
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)

    creds = utils.get_credentials()
    assert creds.token == "fake-token"
    assert creds.scopes == utils.SCOPES


@mock.patch(
    "shipyard_googledocs.utils.service_account.Credentials.from_service_account_file"
)
def test_get_credentials_with_file(mock_from_file, monkeypatch):
    mock_creds = mock.Mock()
    mock_from_file.return_value = mock_creds

    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "/fake/path")
    with mock.patch("os.path.isfile", return_value=True):
        result = utils.get_credentials()
        assert result == mock_creds


@mock.patch(
    "shipyard_googledocs.utils.service_account.Credentials.from_service_account_info"
)
def test_get_credentials_with_json(mock_from_info, monkeypatch):
    mock_creds = mock.Mock()
    mock_from_info.return_value = mock_creds

    json_creds = json.dumps({"type": "service_account"})
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", json_creds)
    with mock.patch("os.path.isfile", return_value=False):
        result = utils.get_credentials()
        assert result == mock_creds


def test_get_credentials_with_bad_json(monkeypatch):
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "{bad_json}")
    monkeypatch.delenv("OAUTH_ACCESS_TOKEN", raising=False)

    with pytest.raises(ExitCodeException) as excinfo:
        utils.get_credentials()
    assert excinfo.value.exit_code == Docs.EXIT_CODE_INVALID_INPUT


def test_get_credentials_with_nothing(monkeypatch):
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    monkeypatch.delenv("OAUTH_ACCESS_TOKEN", raising=False)

    with pytest.raises(ExitCodeException) as excinfo:
        utils.get_credentials()
    assert excinfo.value.exit_code == CloudStorage.EXIT_CODE_UNKNOWN_ERROR
