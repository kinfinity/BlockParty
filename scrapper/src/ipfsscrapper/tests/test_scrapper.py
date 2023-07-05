from unittest import mock

import pytest
import requests

from ipfsscrapper.scrapper.scrapper import Scrapper


@pytest.fixture
def mock_response():
    response = requests.Response()
    response.status_code = 200
    response._content = b'{"name": "Fraction 242"}'
    return response

def test_fetch_metadata_success(mock_response):
    # Create an instance of the Scrapper class
    scrapper = Scrapper("https://blockpartyplatform.mypinata.cloud/ipfs/")

    # Mock the requests.get method and return the mock_response
    with mock.patch('requests.get', return_value=mock_response) as mock_get:
        # Call the fetch_metadata method
        result = scrapper.fetch_metadata("QmamdCZfHLy18hAix12h7ntu41vNjjMGQCj2gEqijiEcRs")

        # Assert that the mock_get method was called with the correct arguments
        mock_get.assert_called_once_with("https://blockpartyplatform.mypinata.cloud/ipfs/QmamdCZfHLy18hAix12h7ntu41vNjjMGQCj2gEqijiEcRs", headers={"Content-Type": "application/json"})

        print(result)
        # Assert that the returned result matches the expected JSON response
        assert result == {"name": "Fraction 242"}

def test_fetch_metadata_failure(mock_response):
    # Create an instance of the Scrapper class
    scrapper = Scrapper("https://blockpartyplatform.mypinata.cloud/ipfs/")

    # Mock the requests.get method and raise an exception
    with mock.patch('requests.get', side_effect=requests.exceptions.RequestException) as mock_get:
        # Call the fetch_metadata method
        result = scrapper.fetch_metadata("asdaf")

        # Assert that the mock_get method was called with the correct arguments
        mock_get.assert_called_once_with("https://blockpartyplatform.mypinata.cloud/ipfs/asdaf", headers={"Content-Type": "application/json"})

        print(result)
        # Assert that the result is None when an exception occurs
        assert result is None
