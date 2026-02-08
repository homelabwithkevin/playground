import json
import os
import pytest
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

"""
    Claude: Yep a bit. No idea what fixture means.
    pytest test.py -v
"""

@pytest.fixture
def base_url():
    """Base URL for the API."""
    return os.getenv('BASE_URL')


@pytest.fixture
def headers():
    """Common headers for API requests."""
    return {
        'Content-Type': 'application/json'
    }


def test_base_endpoint(base_url, headers):
    """Test that the base endpoint returns 200."""
    response = requests.get(base_url, headers=headers)
    assert response.status_code == 200

def test_archive_endpoint(base_url, headers):
    """Test that the archive endpoint returns 200."""
    url = f'{base_url}/archive'
    response = requests.get(url, headers=headers)

    assert response.status_code == 200

def test_emails_endpoint(base_url, headers):
    """Test that the emails endpoint returns 200 and contains 21 items."""
    url = f'{base_url}/emails'
    response = requests.get(url, headers=headers)

    assert response.status_code == 200

    content = json.loads(response.content)
    assert len(content) == 21