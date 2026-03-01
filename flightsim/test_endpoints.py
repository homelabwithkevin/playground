import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')
BASE_URL = BASE_URL.rstrip('/')

class TestRootEndpoint:
    """Test root endpoint."""

    def test_root_returns_html(self):
        """Test that root endpoint returns HTML response."""
        response = requests.get(f'{BASE_URL}/')
        assert response.status_code == 200
        assert 'text/html' in response.headers.get('content-type', '')
        assert 'Flight Sim Calculator' in response.text
        assert 'Airport Search' in response.text
        assert 'Distance Calculator' in response.text
        assert 'Nearest Airports' in response.text


class TestAirportEndpoint:
    """Test airport search endpoint."""

    def test_airport_search_found(self):
        """Test airport search when airport is found."""
        response = requests.get(f'{BASE_URL}/airport/KJFK')
        assert response.status_code == 200
        data = response.json()
        assert data is not None
        assert data['ident'] == 'KJFK'

    def test_airport_search_not_found(self):
        """Test airport search when airport is not found."""
        response = requests.get(f'{BASE_URL}/airport/XXXX')
        assert response.status_code == 200
        data = response.json()
        assert data is None

    def test_airport_search_case_insensitive(self):
        """Test that airport search is case-insensitive."""
        response = requests.get(f'{BASE_URL}/airport/kjfk')
        assert response.status_code == 200
        data = response.json()
        assert data is not None
        assert data['ident'] == 'KJFK'


class TestNearestAirportsEndpoint:
    """Test nearest airports endpoint."""

    def test_nearest_airports_within_range(self):
        """Test finding nearest airports within a specified range."""
        response = requests.get(f'{BASE_URL}/calculate/nearest/KJFK/50')
        assert response.status_code == 200
        data = response.json()
        assert data['source'] == 'KJFK'
        assert 'random' in data
        assert 'all' in data
        assert isinstance(data['random'], list)
        assert isinstance(data['all'], list)
        # Should have at most 10 random airports
        assert len(data['random']) <= 10
        # Source airport should be excluded
        for airport in data['all']:
            assert airport['ident'] != 'KJFK'

    def test_nearest_airports_results_sorted(self):
        """Test that nearest airports results are sorted by distance."""
        response = requests.get(f'{BASE_URL}/calculate/nearest/KJFK/100')
        assert response.status_code == 200
        data = response.json()
        # All results should be sorted by distance
        all_airports = data['all']
        if len(all_airports) > 1:
            distances = [airport['distance_to'] for airport in all_airports]
            assert distances == sorted(distances)

    def test_nearest_airports_large_range(self):
        """Test finding nearest airports with a large range."""
        response = requests.get(f'{BASE_URL}/calculate/nearest/KJFK/100')
        assert response.status_code == 200
        data = response.json()
        assert data['source'] == 'KJFK'
        assert isinstance(data['random'], list)
        assert isinstance(data['all'], list)


class TestEndpointIntegration:
    """Integration tests across multiple endpoints."""

    def test_airport_endpoint_data_format(self):
        """Test that airport endpoint returns expected data fields."""
        response = requests.get(f'{BASE_URL}/airport/KJFK')
        assert response.status_code == 200
        data = response.json()
        assert data is not None
        # Verify expected fields exist
        expected_fields = ['ident', 'name', 'latitude_deg', 'longitude_deg', 'elevation_ft']
        for field in expected_fields:
            assert field in data
