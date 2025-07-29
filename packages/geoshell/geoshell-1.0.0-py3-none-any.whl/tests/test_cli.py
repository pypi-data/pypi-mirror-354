"""
Test cases for GeoShell CLI
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from io import StringIO

# Add the parent directory to the path so we can import geoshell
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from geoshell import cli


class TestGeoShellCLI(unittest.TestCase):
    """Test cases for GeoShell CLI functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_country_result = MagicMock()
        self.mock_country_result.to_dict.return_value = {
            'name': 'Japan',
            'capital': 'Tokyo',
            'population': 125800000,
            'region': 'Asia'
        }
        
        self.mock_weather_result = MagicMock()
        self.mock_weather_result.to_dict.return_value = {
            'location': 'Tokyo',
            'temperature': 22.5,
            'condition': 'Partly Cloudy',
            'humidity': 65
        }
        
        self.mock_holidays_result = [
            MagicMock(to_dict=lambda: {
                'name': 'New Year\'s Day',
                'date': '2024-01-01',
                'type': 'National'
            }),
            MagicMock(to_dict=lambda: {
                'name': 'Christmas Day',
                'date': '2024-12-25',
                'type': 'National'
            })
        ]
    
    @patch('geoshell.core.country')
    @patch('sys.stdout', new_callable=StringIO)
    def test_country_command(self, mock_stdout, mock_country):
        """Test country command execution"""
        mock_country.return_value = self.mock_country_result
        
        # Simulate command line arguments
        test_args = ['country', 'Japan']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass  # CLI may call sys.exit
        
        # Verify country function was called
        mock_country.assert_called_once_with('Japan', None)
        
        # Check output contains expected data
        output = mock_stdout.getvalue()
        self.assertIn('Japan', output)
    
    @patch('geoshell.core.weather')
    @patch('sys.stdout', new_callable=StringIO)
    def test_weather_command(self, mock_stdout, mock_weather):
        """Test weather command execution"""
        mock_weather.return_value = self.mock_weather_result
        
        test_args = ['weather', 'Tokyo']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass
        
        mock_weather.assert_called_once_with('Tokyo', 0)
        
        output = mock_stdout.getvalue()
        self.assertIn('Tokyo', output)
    
    @patch('geoshell.core.holidays')
    @patch('sys.stdout', new_callable=StringIO)
    def test_holidays_command(self, mock_stdout, mock_holidays):
        """Test holidays command execution"""
        mock_holidays.return_value = self.mock_holidays_result
        
        test_args = ['holidays', 'US']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass
        
        mock_holidays.assert_called_once_with('US', None)
        
        output = mock_stdout.getvalue()
        self.assertIn('New Year', output)
    
    @patch('geoshell.core.neighbors')
    @patch('sys.stdout', new_callable=StringIO)
    def test_neighbors_command(self, mock_stdout, mock_neighbors):
        """Test neighbors command execution"""
        mock_neighbors.return_value = ['France', 'Belgium', 'Netherlands']
        
        test_args = ['neighbors', 'Germany']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass
        
        mock_neighbors.assert_called_once_with('Germany')
        
        output = mock_stdout.getvalue()
        self.assertIn('France', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout):
        """Test help command output"""
        test_args = ['--help']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass
        
        output = mock_stdout.getvalue()
        self.assertIn('GeoShell', output)
        self.assertIn('Usage:', output)
        self.assertIn('Commands:', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_version_command(self, mock_stdout):
        """Test version command output"""
        test_args = ['--version']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass
        
        output = mock_stdout.getvalue()
        self.assertIn('GeoShell', output)
        self.assertIn('1.0.0', output)
    
    @patch('geoshell.core.country')
    @patch('sys.stdout', new_callable=StringIO)
    def test_country_with_fields(self, mock_stdout, mock_country):
        """Test country command with specific fields"""
        mock_country.return_value = self.mock_country_result
        
        test_args = ['country', 'Japan', '--fields', 'name,population']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass
        
        # Verify country function was called with fields
        mock_country.assert_called_once_with('Japan', ['name', 'population'])
    
    @patch('geoshell.core.weather')
    @patch('sys.stdout', new_callable=StringIO)
    def test_weather_with_forecast(self, mock_stdout, mock_weather):
        """Test weather command with forecast"""
        mock_weather.return_value = self.mock_weather_result
        
        test_args = ['weather', 'Tokyo', '--forecast', '5']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass
        
        # Verify weather function was called with forecast
        mock_weather.assert_called_once_with('Tokyo', 5)
    
    @patch('geoshell.core.holidays')
    @patch('sys.stdout', new_callable=StringIO)
    def test_holidays_with_year(self, mock_stdout, mock_holidays):
        """Test holidays command with specific year"""
        mock_holidays.return_value = self.mock_holidays_result
        
        test_args = ['holidays', 'US', '--year', '2023']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            try:
                cli.main()
            except SystemExit:
                pass
        
        # Verify holidays function was called with year
        mock_holidays.assert_called_once_with('US', 2023)
    
    @patch('geoshell.core.country')
    def test_output_to_file(self, mock_country):
        """Test saving output to file"""
        mock_country.return_value = self.mock_country_result
        
        test_args = ['country', 'Japan', '--output', 'test_output.json']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
                try:
                    cli.main()
                except SystemExit:
                    pass
                
                # Verify file was opened for writing
                mock_file.assert_called_once_with('test_output.json', 'w')
    
    @patch('geoshell.core.country')
    @patch('sys.stderr', new_callable=StringIO)
    def test_error_handling(self, mock_stderr, mock_country):
        """Test CLI error handling"""
        mock_country.side_effect = Exception("Test error")
        
        test_args = ['country', 'Japan']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            with self.assertRaises(SystemExit):
                cli.main()
        
        # Check error was printed to stderr
        error_output = mock_stderr.getvalue()
        self.assertIn('Error:', error_output)
        self.assertIn('Test error', error_output)
    
    @patch('geoshell.core.country')
    @patch('sys.stderr', new_callable=StringIO)
    def test_verbose_error_handling(self, mock_stderr, mock_country):
        """Test CLI verbose error handling"""
        mock_country.side_effect = Exception("Test error")
        
        test_args = ['country', 'Japan', '--verbose']
        
        with patch('sys.argv', ['geoshell'] + test_args):
            with self.assertRaises(SystemExit):
                cli.main()
        
        # Check that traceback is included in verbose mode
        error_output = mock_stderr.getvalue()
        self.assertIn('Traceback', error_output)


class TestCLIFormatting(unittest.TestCase):
    """Test cases for CLI output formatting"""
    
    def test_format_json(self):
        """Test JSON output formatting"""
        data = {'name': 'Japan', 'population': 125800000}
        result = cli.format_output(data, 'json')
        
        self.assertIsInstance(result, str)
        # Should be valid JSON
        import json
        parsed = json.loads(result)
        self.assertEqual(parsed['name'], 'Japan')
    
    def test_format_table(self):
        """Test table output formatting"""
        data = [
            {'country': 'Japan', 'population': 125800000},
            {'country': 'Germany', 'population': 83240000}
        ]
        result = cli.format_output(data, 'table')
        
        # Implementation would need to be completed in cli.py
        # This is a placeholder test
        self.assertIsInstance(result, str)
    
    def test_format_csv(self):
        """Test CSV output formatting"""
        data = [
            {'country': 'Japan', 'population': 125800000},
            {'country': 'Germany', 'population': 83240000}
        ]
        result = cli.format_output(data, 'csv')
        
        # Implementation would need to be completed in cli.py
        # This is a placeholder test
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    # Run the CLI tests
    unittest.main(verbosity=2)
