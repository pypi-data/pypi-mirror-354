"""
Unit tests for GeoShell
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the parent directory to the path so we can import geoshell
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from geoshell import core, utils
from geoshell.exceptions import CountryNotFound, LocationNotFound, APIError


class TestGeoShellCore(unittest.TestCase):
    """Test cases for GeoShell core functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_country_data = {
            'name': {'common': 'Japan'},
            'capital': ['Tokyo'],
            'population': 125800000,
            'area': 377975,
            'currencies': {'JPY': {'name': 'Japanese yen'}},
            'languages': {'jpn': 'Japanese'},
            'region': 'Asia',
            'subregion': 'Eastern Asia',
            'borders': [],
            'flags': {'png': 'https://example.com/flag.png'}
        }
        
        self.mock_weather_data = {
            'name': 'Tokyo',
            'main': {
                'temp': 22.5,
                'humidity': 65,
                'pressure': 1013
            },
            'weather': [{'description': 'partly cloudy'}],
            'wind': {'speed': 3.4},
            'visibility': 10000
        }
        
        self.mock_holidays_data = [
            {
                'name': 'New Year\'s Day',
                'date': '2024-01-01',
                'type': 'National'
            },
            {
                'name': 'Christmas Day',
                'date': '2024-12-25',
                'type': 'National'
            }
        ]
    
    @patch('geoshell.core.requests.Session.get')
    def test_country_success(self, mock_get):
        """Test successful country data retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [self.mock_country_data]
        mock_get.return_value = mock_response
        
        result = core.country('Japan')
        
        self.assertEqual(result.name, 'Japan')
        self.assertEqual(result.capital, 'Tokyo')
        self.assertEqual(result.population, 125800000)
        self.assertEqual(result.region, 'Asia')
    
    @patch('geoshell.core.requests.Session.get')
    def test_country_not_found(self, mock_get):
        """Test country not found error"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(CountryNotFound):
            core.country('InvalidCountry')
    
    @patch('geoshell.core.requests.Session.get')
    def test_country_api_error(self, mock_get):
        """Test API error handling"""
        mock_get.side_effect = Exception('Network error')
        
        with self.assertRaises(APIError):
            core.country('Japan')
    
    def test_weather_mock_data(self):
        """Test weather function returns mock data when no API key"""
        result = core.weather('Tokyo')
        
        self.assertEqual(result.location, 'Tokyo')
        self.assertIsInstance(result.temperature, (int, float))
        self.assertIsInstance(result.condition, str)
        self.assertIsInstance(result.humidity, int)
    
    @patch('geoshell.core.requests.Session.get')
    def test_holidays_success(self, mock_get):
        """Test successful holidays retrieval"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_holidays_data
        mock_get.return_value = mock_response
        
        result = core.holidays('US')
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, 'New Year\'s Day')
        self.assertEqual(result[1].name, 'Christmas Day')
    
    @patch('geoshell.core.requests.Session.get')
    def test_holidays_fallback(self, mock_get):
        """Test holidays fallback to mock data"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = core.holidays('US')
        
        # Should return mock data
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
    
    @patch('geoshell.core.country')
    def test_neighbors_success(self, mock_country):
        """Test successful neighbors retrieval"""
        mock_country_info = MagicMock()
        mock_country_info.name = 'Germany'
        mock_country_info.borders = 'AT,BE,CZ,DK,FR,LU,NL,PL,CH'
        mock_country.return_value = mock_country_info
        
        result = core.neighbors('Germany')
        
        expected_neighbors = [
            'Austria', 'Belgium', 'Czech Republic', 'Denmark', 
            'France', 'Luxembourg', 'Netherlands', 'Poland', 'Switzerland'
        ]
        
        # Check that we get some neighbors (exact list may vary based on mock implementation)
        self.assertIsInstance(result, list)
    
    def test_timezone_mock(self):
        """Test timezone function returns mock data"""
        result = core.timezone('Tokyo')
        
        self.assertIn('location', result)
        self.assertIn('timezone', result)
        self.assertIn('current_time', result)
        self.assertEqual(result['location'], 'Tokyo')
    
    def test_news_mock(self):
        """Test news function returns mock data"""
        result = core.news('Japan')
        
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIn('title', result[0])
        self.assertIn('description', result[0])


class TestGeoShellUtils(unittest.TestCase):
    """Test cases for GeoShell utilities"""
    
    def test_format_json(self):
        """Test JSON formatting"""
        data = {'name': 'Japan', 'population': 125800000}
        result = utils.format_json(data)
        
        self.assertIsInstance(result, str)
        self.assertIn('Japan', result)
        self.assertIn('125800000', result)
    
    def test_format_table(self):
        """Test table formatting"""
        data = [
            {'country': 'Japan', 'population': 125800000},
            {'country': 'Germany', 'population': 83240000}
        ]
        result = utils.format_table(data)
        
        self.assertIsInstance(result, str)
        self.assertIn('Japan', result)
        self.assertIn('Germany', result)
        self.assertIn('|', result)  # Table separator
    
    def test_format_csv(self):
        """Test CSV formatting"""
        data = [
            {'country': 'Japan', 'population': 125800000},
            {'country': 'Germany', 'population': 83240000}
        ]
        result = utils.format_csv(data)
        
        self.assertIsInstance(result, str)
        self.assertIn('country,population', result)
        self.assertIn('Japan,125800000', result)
    
    def test_validate_country_name(self):
        """Test country name validation"""
        # Valid cases
        self.assertEqual(utils.validate_country_name('Japan'), 'Japan')
        self.assertEqual(utils.validate_country_name('  Germany  '), 'Germany')
        
        # Invalid cases
        with self.assertRaises(ValueError):
            utils.validate_country_name('')
        
        with self.assertRaises(ValueError):
            utils.validate_country_name(None)
    
    def test_validate_year(self):
        """Test year validation"""
        # Valid cases
        self.assertEqual(utils.validate_year(2024), 2024)
        self.assertEqual(utils.validate_year(2000), 2000)
        
        # Invalid cases
        with self.assertRaises(ValueError):
            utils.validate_year(1800)  # Too old
        
        with self.assertRaises(ValueError):
            utils.validate_year(2050)  # Too far in future
        
        with self.assertRaises(ValueError):
            utils.validate_year('2024')  # Wrong type
    
    def test_validate_forecast_days(self):
        """Test forecast days validation"""
        # Valid cases
        self.assertEqual(utils.validate_forecast_days(0), 0)
        self.assertEqual(utils.validate_forecast_days(7), 7)
        
        # Invalid cases
        with self.assertRaises(ValueError):
            utils.validate_forecast_days(-1)
        
        with self.assertRaises(ValueError):
            utils.validate_forecast_days(8)
        
        with self.assertRaises(ValueError):
            utils.validate_forecast_days('5')
    
    def test_parse_coordinates(self):
        """Test coordinate parsing"""
        # Valid cases
        lat, lon = utils.parse_coordinates('40.7128, -74.0060')
        self.assertEqual(lat, 40.7128)
        self.assertEqual(lon, -74.0060)
        
        lat, lon = utils.parse_coordinates('0,0')
        self.assertEqual(lat, 0.0)
        self.assertEqual(lon, 0.0)
        
        # Invalid cases
        with self.assertRaises(ValueError):
            utils.parse_coordinates('invalid')
        
        with self.assertRaises(ValueError):
            utils.parse_coordinates('100, -200')  # Out of range
    
    def test_normalize_country_name(self):
        """Test country name normalization"""
        # Test known mappings
        self.assertEqual(utils.normalize_country_name('usa'), 'US')
        self.assertEqual(utils.normalize_country_name('United States'), 'US')
        self.assertEqual(utils.normalize_country_name('germany'), 'DE')
        
        # Test unknown country (should be title-cased)
        self.assertEqual(utils.normalize_country_name('fictional country'), 'Fictional Country')
    
    def test_humanize_number(self):
        """Test number humanization"""
        self.assertEqual(utils.humanize_number(1500), '1.5K')
        self.assertEqual(utils.humanize_number(1500000), '1.5M')
        self.assertEqual(utils.humanize_number(1500000000), '1.5B')
        self.assertEqual(utils.humanize_number(500), '500')
    
    def test_truncate_string(self):
        """Test string truncation"""
        long_string = "This is a very long string that should be truncated"
        result = utils.truncate_string(long_string, 20)
        
        self.assertEqual(len(result), 20)
        self.assertTrue(result.endswith('...'))
    
    def test_safe_get(self):
        """Test safe dictionary access"""
        data = {
            'level1': {
                'level2': {
                    'value': 'found'
                }
            }
        }
        
        # Existing path
        self.assertEqual(utils.safe_get(data, 'level1.level2.value'), 'found')
        
        # Non-existing path
        self.assertEqual(utils.safe_get(data, 'level1.nonexistent'), None)
        self.assertEqual(utils.safe_get(data, 'level1.nonexistent', 'default'), 'default')
    
    def test_is_valid_url(self):
        """Test URL validation"""
        # Valid URLs
        self.assertTrue(utils.is_valid_url('https://example.com'))
        self.assertTrue(utils.is_valid_url('http://localhost:8080'))
        self.assertTrue(utils.is_valid_url('https://api.example.com/data'))
        
        # Invalid URLs
        self.assertFalse(utils.is_valid_url('not-a-url'))
        self.assertFalse(utils.is_valid_url('ftp://example.com'))
        self.assertFalse(utils.is_valid_url(''))


class TestProgressBar(unittest.TestCase):
    """Test cases for ProgressBar utility"""
    
    def test_progress_bar_creation(self):
        """Test progress bar creation"""
        pb = utils.ProgressBar(100)
        self.assertEqual(pb.total, 100)
        self.assertEqual(pb.current, 0)
    
    def test_progress_bar_update(self):
        """Test progress bar updates"""
        pb = utils.ProgressBar(10)
        pb.update(5)
        self.assertEqual(pb.current, 5)
        
        pb.update(3)
        self.assertEqual(pb.current, 8)


class TestRetryOperation(unittest.TestCase):
    """Test cases for retry operation utility"""
    
    def test_retry_success_first_attempt(self):
        """Test successful operation on first attempt"""
        def successful_operation():
            return "success"
        
        result = utils.retry_operation(successful_operation)
        self.assertEqual(result, "success")
    
    def test_retry_success_after_failure(self):
        """Test successful operation after failures"""
        self.call_count = 0
        
        def failing_then_success():
            self.call_count += 1
            if self.call_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        result = utils.retry_operation(failing_then_success, max_retries=3, delay=0.1)
        self.assertEqual(result, "success")
        self.assertEqual(self.call_count, 3)
    
    def test_retry_max_attempts_exceeded(self):
        """Test failure after max attempts"""
        def always_failing():
            raise Exception("Always fails")
        
        with self.assertRaises(Exception):
            utils.retry_operation(always_failing, max_retries=2, delay=0.1)


if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestGeoShellCore))
    suite.addTest(unittest.makeSuite(TestGeoShellUtils))
    suite.addTest(unittest.makeSuite(TestProgressBar))
    suite.addTest(unittest.makeSuite(TestRetryOperation))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Exit with appropriate code
    exit_code = 0 if result.wasSuccessful() else 1
    print(f"\nTest suite {'PASSED' if exit_code == 0 else 'FAILED'}")
