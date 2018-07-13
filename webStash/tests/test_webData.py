import pytest
import os

try:
    from webData import WebData
except (SystemError, ImportError):
    from .webData import WebData

@pytest.fixture()
def mock_webData():
    return WebData('GUID', 'https://www.website.com', '<some html tags>')

def test_to_df(mock_webData):
    mock_webData.to_csv()
    assert os.path.isfile('GUID.csv')
    os.remove('GUID.csv')

def test_to_json(mock_webData):
    mock_webData.to_json()
    assert os.path.isfile('GUID.json')
    os.remove('GUID.json')
