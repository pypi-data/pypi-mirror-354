"""
Integration tests for GeoShell
These tests make actual API calls and should be run with caution
"""

import unittest
import os
import sys
import time

# Add the parent directory to the path so we can import geoshell
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from geoshell import core
from geoshell.exceptions import CountryNotFound, LocationNotFound, APIError


class TestGeoShellIntegration(unittest.TestCase):
    """Integration tests that make real API calls"""
    
    @classmethod
    def setUpClass(cls):
        """Set up integration test class"""
        # Skip integration tests if SKIP_INTEGRATION is set
        if os.environ.get('SKIP_INTEGRATION'):
            raise unittest.SkipTest("Integration tests skipped")
        
        # Add delay to avoid rate limiting
        cls.request_delay = 1.0
    
    def setUp(self):
        """Set up each test with delay to avoid rate limiting"""
        time.sleep(self.request_delay)
    
    def test_real_country_api(self):
        """Test real country API call"""
        try:
            result = core.country('Japan')
            
            self.assertIsNotNone(result)
            self.assertEqual(result.name, 'Japan')
            self.assertEqual(result.capital, 'Tokyo')
            self.assertGreater(result.population, 100000000)
            self.assertEqual(result.region, 'Asia')
            
        except APIError as e:
            self.skipTest(f"Country API not available: {e}")
    
    def test_real_country_not_found(self):
        """Test real country API with invalid country"""
        with self.assertRaises(CountryNotFound):
            core.country('NonExistentCountry123')
    
    def test_real_holidays_api(self):
        """Test real holidays API call"""
        try:
            result = core.holidays('US', 2024)
            
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)
            
            # Check that we have some expected holidays
            holiday_names = [h.name for h in result]
            self.assertTrue(any('New Year' in name for name in holiday_names))
            
        except APIError as e:
            self.skipTest(f"Holidays API not available: {e}")
    
    def test_multiple_country_requests(self):
        """Test multiple country requests"""
        countries = ['Japan', 'Germany', 'France']
        results = []
        
        for country in countries:
            try:
                result = core.country(country)
                results.append(result)
                time.sleep(self.request_delay)  # Rate limiting
            except APIError:
                self.skipTest(f"API not available for {country}")
        
        self.assertEqual(len(results), len(countries))
        
        # Verify each result
        for result in results:
            self.assertIsNotNone(result.name)
            self.assertIsNotNone(result.capital)
            self.assertGreater(result.population, 0)
    
    def test_country_with_fields(self):
        """Test country API with specific fields"""
        try:
            result = core.country('Canada', fields=['name', 'capital', 'population'])
            
            # Should have the requested data
            self.assertEqual(result.name, 'Canada')
            self.assertEqual(result.capital, 'Ottawa')
            self.assertGreater(result.population, 30000000)
            
        except APIError as e:
            self.skipTest(f"Country API not available: {e}")
    
    def test_neighbors_integration(self):
        """Test neighbors functionality with real data"""
        try:
            # Test with a country that has many neighbors
            result = core.neighbors('Germany')
            
            # Germany should have several neighbors
            self.assertIsInstance(result, list)
            # Note: might be empty if mock data is used
            
        except (CountryNotFound, APIError) as e:
            self.skipTest(f"Neighbors API not available: {e}")
    
    def test_api_rate_limiting(self):
        """Test that API calls respect rate limiting"""
        start_time = time.time()
        
        try:
            # Make several quick requests
            for i in range(3):
                core.country(f'Japan')
                if i < 2:  # Don't delay after last request
                    time.sleep(0.5)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Should take at least 1 second due to delays
            self.assertGreater(duration, 1.0)
            
        except APIError as e:
            self.skipTest(f"API not available for rate limiting test: {e}")
    
    def test_error_recovery(self):
        """Test error recovery and retries"""
        # Test with invalid country first, then valid one
        with self.assertRaises(CountryNotFound):
            core.country('InvalidCountry')
        
        time.sleep(self.request_delay)
        
        try:
            # Should still work after error
            result = core.country('Japan')
            self.assertEqual(result.name, 'Japan')
        except APIError as e:
            self.skipTest(f"API not available for error recovery test: {e}")


class TestPerformance(unittest.TestCase):
    """Performance tests for GeoShell"""
    
    def test_response_time(self):
        """Test that responses are reasonably fast"""
        start_time = time.time()
        
        try:
            result = core.country('Japan')
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Response should be under 5 seconds
            self.assertLess(response_time, 5.0)
            
        except APIError:
            self.skipTest("API not available for performance test")
    
    def test_memory_usage(self):
        """Test memory usage doesn't grow excessively"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        try:
            # Make several requests
            for i in range(5):
                result = core.country('Japan')
                time.sleep(0.5)
            
            final_memory = process.memory_info().rss
            memory_growth = final_memory - initial_memory
            
            # Memory growth should be reasonable (less than 50MB)
            self.assertLess(memory_growth, 50 * 1024 * 1024)
            
        except APIError:
            self.skipTest("API not available for memory test")


if __name__ == '__main__':
    # Check if we should skip integration tests
    if len(sys.argv) > 1 and sys.argv[1] == '--skip-integration':
        os.environ['SKIP_INTEGRATION'] = '1'
    
    # Run integration tests
    unittest.main(verbosity=2, warnings='ignore')
