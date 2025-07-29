"""
Utility functions for GeoShell
"""

import csv
import json
import sys
from io import StringIO
from typing import Any, Dict, List, Union
from datetime import datetime


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as JSON string"""
    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)


def format_table(data: Union[Dict, List[Dict]], headers: List[str] = None) -> str:
    """Format data as a table string"""
    if not data:
        return "No data available"
    
    # Handle single dict
    if isinstance(data, dict):
        data = [data]
    
    # Handle list of objects with to_dict method
    if hasattr(data[0], 'to_dict'):
        data = [item.to_dict() for item in data]
    
    if not headers:
        headers = list(data[0].keys()) if data else []
    
    # Calculate column widths
    col_widths = {}
    for header in headers:
        col_widths[header] = len(str(header))
        for row in data:
            value = str(row.get(header, ''))
            col_widths[header] = max(col_widths[header], len(value))
    
    # Build table
    table_lines = []
    
    # Header row
    header_row = " | ".join(
        str(header).ljust(col_widths[header]) for header in headers
    )
    table_lines.append(header_row)
    
    # Separator row
    separator = " | ".join("-" * col_widths[header] for header in headers)
    table_lines.append(separator)
    
    # Data rows
    for row in data:
        data_row = " | ".join(
            str(row.get(header, '')).ljust(col_widths[header]) for header in headers
        )
        table_lines.append(data_row)
    
    return "\n".join(table_lines)


def format_csv(data: Union[Dict, List[Dict]], headers: List[str] = None) -> str:
    """Format data as CSV string"""
    if not data:
        return ""
    
    # Handle single dict
    if isinstance(data, dict):
        data = [data]
    
    # Handle list of objects with to_dict method
    if hasattr(data[0], 'to_dict'):
        data = [item.to_dict() for item in data]
    
    if not headers:
        headers = list(data[0].keys()) if data else []
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    
    for row in data:
        # Convert all values to strings and handle None
        csv_row = {}
        for header in headers:
            value = row.get(header, '')
            if isinstance(value, list):
                value = '; '.join(str(v) for v in value)
            csv_row[header] = str(value) if value is not None else ''
        writer.writerow(csv_row)
    
    return output.getvalue()


def validate_country_name(country: str) -> str:
    """Validate and normalize country name"""
    if not country or not isinstance(country, str):
        raise ValueError("Country name must be a non-empty string")
    
    return country.strip()


def validate_location(location: str) -> str:
    """Validate and normalize location name"""
    if not location or not isinstance(location, str):
        raise ValueError("Location must be a non-empty string")
    
    return location.strip()


def validate_year(year: int) -> int:
    """Validate year parameter"""
    current_year = datetime.now().year
    
    if not isinstance(year, int):
        raise ValueError("Year must be an integer")
    
    if year < 1900 or year > current_year + 10:
        raise ValueError(f"Year must be between 1900 and {current_year + 10}")
    
    return year


def validate_forecast_days(days: int) -> int:
    """Validate forecast days parameter"""
    if not isinstance(days, int):
        raise ValueError("Forecast days must be an integer")
    
    if days < 0 or days > 7:
        raise ValueError("Forecast days must be between 0 and 7")
    
    return days


def parse_coordinates(coord_string: str) -> tuple:
    """Parse coordinate string into latitude and longitude"""
    try:
        parts = coord_string.split(',')
        if len(parts) != 2:
            raise ValueError("Coordinates must be in format 'lat,lon'")
        
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
        
        if lat < -90 or lat > 90:
            raise ValueError("Latitude must be between -90 and 90")
        
        if lon < -180 or lon > 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        return lat, lon
    
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid coordinates format: {e}")


def get_country_code_mapping() -> Dict[str, str]:
    """Get mapping of country names to ISO codes"""
    return {
        'usa': 'US',
        'united states': 'US',
        'united states of america': 'US',
        'america': 'US',
        'canada': 'CA',
        'germany': 'DE',
        'deutschland': 'DE',
        'france': 'FR',
        'japan': 'JP',
        'nippon': 'JP',
        'brazil': 'BR',
        'brasil': 'BR',
        'uk': 'GB',
        'united kingdom': 'GB',
        'great britain': 'GB',
        'britain': 'GB',
        'england': 'GB',
        'italy': 'IT',
        'italia': 'IT',
        'spain': 'ES',
        'españa': 'ES',
        'australia': 'AU',
        'india': 'IN',
        'china': 'CN',
        'russia': 'RU',
        'mexico': 'MX',
        'netherlands': 'NL',
        'holland': 'NL',
        'belgium': 'BE',
        'switzerland': 'CH',
        'austria': 'AT',
        'sweden': 'SE',
        'norway': 'NO',
        'denmark': 'DK',
        'finland': 'FI',
        'poland': 'PL',
        'czech republic': 'CZ',
        'czechia': 'CZ',
        'slovakia': 'SK',
        'hungary': 'HU',
        'romania': 'RO',
        'bulgaria': 'BG',
        'croatia': 'HR',
        'slovenia': 'SI',
        'serbia': 'RS',
        'bosnia': 'BA',
        'montenegro': 'ME',
        'albania': 'AL',
        'greece': 'GR',
        'turkey': 'TR',
        'portugal': 'PT',
        'ireland': 'IE',
        'iceland': 'IS',
        'south korea': 'KR',
        'north korea': 'KP',
        'thailand': 'TH',
        'vietnam': 'VN',
        'singapore': 'SG',
        'malaysia': 'MY',
        'indonesia': 'ID',
        'philippines': 'PH',
        'taiwan': 'TW',
        'hong kong': 'HK',
        'israel': 'IL',
        'saudi arabia': 'SA',
        'uae': 'AE',
        'united arab emirates': 'AE',
        'egypt': 'EG',
        'south africa': 'ZA',
        'nigeria': 'NG',
        'kenya': 'KE',
        'morocco': 'MA',
        'algeria': 'DZ',
        'argentina': 'AR',
        'chile': 'CL',
        'colombia': 'CO',
        'peru': 'PE',
        'venezuela': 'VE',
        'ecuador': 'EC',
        'uruguay': 'UY',
        'paraguay': 'PY',
        'bolivia': 'BO',
        'new zealand': 'NZ',
    }


def normalize_country_name(country: str) -> str:
    """Normalize country name to standard format"""
    if not country:
        return country
    
    # Convert to lowercase for mapping lookup
    country_lower = country.lower().strip()
    
    # Try to get ISO code from mapping
    mapping = get_country_code_mapping()
    if country_lower in mapping:
        return mapping[country_lower]
    
    # If not found in mapping, return original (capitalized)
    return country.strip().title()


def log_error(error: Exception, context: str = None) -> None:
    """Log error with context information"""
    timestamp = datetime.now().isoformat()
    error_msg = f"[{timestamp}] ERROR"
    
    if context:
        error_msg += f" in {context}"
    
    error_msg += f": {type(error).__name__}: {str(error)}"
    
    print(error_msg, file=sys.stderr)


def safe_get(data: dict, key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with nested key support"""
    if '.' not in key:
        return data.get(key, default)
    
    keys = key.split('.')
    current = data
    
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    
    return current


def humanize_number(number: Union[int, float]) -> str:
    """Convert number to human-readable format"""
    if not isinstance(number, (int, float)):
        return str(number)
    
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(int(number))


def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate string with ellipsis if too long"""
    if not isinstance(text, str):
        text = str(text)
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    import re
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None


class ProgressBar:
    """Simple progress bar for CLI operations"""
    
    def __init__(self, total: int, width: int = 50, prefix: str = "Progress"):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.current = 0
    
    def update(self, amount: int = 1) -> None:
        """Update progress bar"""
        self.current += amount
        self._print_bar()
    
    def _print_bar(self) -> None:
        """Print the progress bar"""
        if self.total == 0:
            return
        
        percent = self.current / self.total
        filled_width = int(self.width * percent)
        bar = '█' * filled_width + '-' * (self.width - filled_width)
        
        print(f'\r{self.prefix}: |{bar}| {percent:.1%}', end='', flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete


def retry_operation(func, max_retries: int = 3, delay: float = 1.0):
    """Retry an operation with exponential backoff"""
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            wait_time = delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...", file=sys.stderr)
            time.sleep(wait_time)
