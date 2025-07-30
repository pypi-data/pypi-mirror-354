import os
import pytest
from unittest import mock
from shipyard_googledocs.cli.download import download_google_docs_file
from shipyard_googledocs import exceptions


@pytest.fixture
def mock_doc_id():
    return "123fakeDocID456"


@pytest.fixture
def mock_doc_service():
    mock_docs_service = mock.Mock()
    mock_docs_service.documents.return_value.get.return_value.execute.return_value = {
        "body": {
            "content": [
                {
                    "paragraph": {
                        "elements": [
                            {"textRun": {"content": "This is a test paragraph."}},
                        ]
                    }
                }
            ]
        }
    }
    return mock_docs_service


@pytest.fixture
def empty_doc_service():
    mock_docs_service = mock.Mock()
    mock_docs_service.documents.return_value.get.return_value.execute.return_value = {
        "body": {"content": []}
    }
    return mock_docs_service


@mock.patch("shipyard_googledocs.cli.download.utils.extract_doc_id_from_url")
def test_successful_download(mock_extract, mock_doc_service, tmp_path, mock_doc_id):
    mock_extract.return_value = mock_doc_id
    destination = tmp_path / "output.txt"

    download_google_docs_file(
        docs_service=mock_doc_service,
        doc_url="https://docs.google.com/document/d/fakeID123/edit",
        destination_path=str(destination),
    )

    assert destination.exists()
    assert "This is a test paragraph." in destination.read_text()


@mock.patch("shipyard_googledocs.cli.download.utils.extract_doc_id_from_url")
def test_download_raises_for_invalid_url(mock_extract):
    mock_extract.return_value = None
    with pytest.raises(exceptions.InvalidDocUrlError):
        download_google_docs_file(
            docs_service=mock.Mock(),
            doc_url="not_a_valid_doc_url",
            destination_path="doesnt_matter.txt",
        )


@mock.patch("shipyard_googledocs.cli.download.utils.extract_doc_id_from_url")
def test_download_raises_for_empty_doc(
    mock_extract, empty_doc_service, mock_doc_id, tmp_path
):
    mock_extract.return_value = mock_doc_id
    dest_path = tmp_path / "empty.txt"

    with pytest.raises(exceptions.DownloadError) as excinfo:
        download_google_docs_file(
            docs_service=empty_doc_service,
            doc_url="https://docs.google.com/document/d/empty/edit",
            destination_path=str(dest_path),
        )

    assert "is empty" in str(excinfo.value)


@mock.patch("shipyard_googledocs.cli.download.utils.extract_doc_id_from_url")
def test_download_handles_api_exception(mock_extract, mock_doc_id):
    mock_extract.return_value = mock_doc_id
    mock_service = mock.Mock()
    mock_service.documents.return_value.get.return_value.execute.side_effect = (
        Exception("Google API died")
    )

    with pytest.raises(exceptions.DownloadError) as excinfo:
        download_google_docs_file(
            docs_service=mock_service,
            doc_url="https://docs.google.com/document/d/failure/edit",
            destination_path="fail.txt",
        )
    assert "Google API died" in str(excinfo.value)
