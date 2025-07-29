"""
GeoShell Core Implementation
A Python library for fetching real-time geo-data
"""

import json
import requests
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

# Configuration
BASE_URLS = {
    'countries': 'https://restcountries.com/v3.1',
    'weather': 'https://api.openweathermap.org/data/2.5',
    'holidays': 'https://date.nager.at/api/v3',
    'news': 'https://newsapi.org/v2'
}

@dataclass
class CountryInfo:
    """Country information data class"""
    name: str
    capital: str
    population: int
    area: float
    currency: str
    languages: List[str]
    region: str
    subregion: str
    borders: List[str]
    flag: str
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'capital': self.capital,
            'population': self.population,
            'area': self.area,
            'currency': self.currency,
            'languages': self.languages,
            'region': self.region,
            'subregion': self.subregion,
            'borders': self.borders,
            'flag': self.flag
        }

@dataclass
class WeatherInfo:
    """Weather information data class"""
    location: str
    temperature: float
    condition: str
    humidity: int
    wind_speed: float
    pressure: int
    visibility: float
    uv_index: int
    
    def to_dict(self) -> Dict:
        return {
            'location': self.location,
            'temperature': self.temperature,
            'condition': self.condition,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'pressure': self.pressure,
            'visibility': self.visibility,
            'uv_index': self.uv_index
        }

@dataclass
class Holiday:
    """Holiday information data class"""
    name: str
    date: str
    type: str
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'date': self.date,
            'type': self.type
        }

class GeoShellError(Exception):
    """Base exception for GeoShell"""
    pass

class CountryNotFound(GeoShellError):
    """Raised when country is not found"""
    pass

class LocationNotFound(GeoShellError):
    """Raised when location is not found"""
    pass

class APIError(GeoShellError):
    """Raised when API request fails"""
    pass

class GeoShell:
    """Main GeoShell class"""
    
    def __init__(self, weather_api_key: Optional[str] = None):
        self.weather_api_key = weather_api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GeoShell/1.0.0'
        })
    
    def country(self, name: str, fields: Optional[List[str]] = None) -> CountryInfo:
        """
        Get country information
        
        Args:
            name: Country name or ISO code
            fields: Specific fields to return
            
        Returns:
            CountryInfo object
            
        Raises:
            CountryNotFound: If country is not found
            APIError: If API request fails
        """
        try:
            url = f"{BASE_URLS['countries']}/name/{name}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 404:
                raise CountryNotFound(f"Country '{name}' not found")
            
            response.raise_for_status()
            data = response.json()[0]  # Take first result
            
            # Extract country information
            country_info = CountryInfo(
                name=data.get('name', {}).get('common', name),
                capital=data.get('capital', ['Unknown'])[0] if data.get('capital') else 'Unknown',
                population=data.get('population', 0),
                area=data.get('area', 0),
                currency=list(data.get('currencies', {}).keys())[0] if data.get('currencies') else 'Unknown',
                languages=list(data.get('languages', {}).values()) if data.get('languages') else ['Unknown'],
                region=data.get('region', 'Unknown'),
                subregion=data.get('subregion', 'Unknown'),
                borders=data.get('borders', []),
                flag=data.get('flags', {}).get('png', '')
            )
            
            return country_info
            
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch country data: {str(e)}")
    
    def weather(self, location: str, forecast: int = 0) -> WeatherInfo:
        """
        Get weather information
        
        Args:
            location: City name or coordinates
            forecast: Number of forecast days (0-7) 
            location: City name or coordinates
            forecast: Number of forecast days (0-7)
            
        Returns:
            WeatherInfo object
            
        Raises:
            LocationNotFound: If location is not found
            APIError: If API request fails
        """
        if not self.weather_api_key:
            # Mock weather data for demo purposes
            return WeatherInfo(
                location=location,
                temperature=22.5,
                condition="Partly Cloudy",
                humidity=65,
                wind_speed=12.3,
                pressure=1013,
                visibility=10.0,
                uv_index=5
            )
        
        try:
            url = f"{BASE_URLS['weather']}/weather"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 404:
                raise LocationNotFound(f"Location '{location}' not found")
            
            response.raise_for_status()
            data = response.json()
            
            weather_info = WeatherInfo(
                location=data['name'],
                temperature=data['main']['temp'],
                condition=data['weather'][0]['description'].title(),
                humidity=data['main']['humidity'],
                wind_speed=data['wind']['speed'],
                pressure=data['main']['pressure'],
                visibility=data.get('visibility', 0) / 1000,  # Convert to km
                uv_index=0  # Would need separate UV API call
            )
            
            return weather_info
            
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch weather data: {str(e)}")
    
    def holidays(self, country: str, year: Optional[int] = None) -> List[Holiday]:
        """
        Get national holidays for a country
        
        Args:
            country: Country name or ISO code
            year: Year to get holidays for (default: current year)
            
        Returns:
            List of Holiday objects
            
        Raises:
            CountryNotFound: If country is not found
            APIError: If API request fails
        """
        if year is None:
            year = datetime.now().year
        
        try:
            # Convert country name to ISO code if needed
            country_code = self._get_country_code(country)
            
            url = f"{BASE_URLS['holidays']}/PublicHolidays/{year}/{country_code}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 404:
                raise CountryNotFound(f"Holidays for '{country}' not found")
            
            response.raise_for_status()
            data = response.json()
            
            holidays = []
            for holiday_data in data:
                holiday = Holiday(
                    name=holiday_data['name'],
                    date=holiday_data['date'],
                    type=holiday_data.get('type', 'National')
                )
                holidays.append(holiday)
            
            return holidays
            
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch holidays data: {str(e)}")
    
    def neighbors(self, country: str) -> List[str]:
        """
        Get neighboring countries
        
        Args:
            country: Country name or ISO code
            
        Returns:
            List of neighboring country names
            
        Raises:
            CountryNotFound: If country is not found
            APIError: If API request fails
        """
        try:
            country_info = self.country(country)
            
            if not country_info.borders:
                return []
            
            # Convert border codes to country names
            neighbor_names = []
            for border_code in country_info.borders:
                try:
                    neighbor_info = self.country(border_code)
                    neighbor_names.append(neighbor_info.name)
                except (CountryNotFound, APIError):
                    # Skip if we can't resolve the border code
                    continue
            
            return neighbor_names
            
        except (CountryNotFound, APIError) as e:
            raise e
    
    def timezone(self, location: str) -> Dict:
        """
        Get timezone information for a location
        
        Args:
            location: City name or coordinates
            
        Returns:
            Dictionary with timezone information
        """
        # Mock implementation - would use timezone API in real version
        return {
            'location': location,
            'timezone': 'UTC+0',
            'current_time': datetime.now().isoformat(),
            'offset': '+00:00'
        }
    
    def news(self, country: str, limit: int = 10) -> List[Dict]:
        """
        Get latest news for a country
        
        Args:
            country: Country name
            limit: Number of articles to return
            
        Returns:
            List of news articles
        """
        # Mock implementation - would use news API in real version
        return [
            {
                'title': f'Latest news from {country}',
                'description': 'Mock news article description',
                'url': 'https://example.com/news',
                'published_at': datetime.now().isoformat(),
                'source': 'Mock News'
            }
        ]
    
    def _get_country_code(self, country: str) -> str:
        """Convert country name to ISO code"""
        # Simplified mapping - would use comprehensive lookup in real version
        country_codes = {
            'usa': 'US',
            'united states': 'US',
            'canada': 'CA',
            'germany': 'DE',
            'france': 'FR',
            'japan': 'JP',
            'brazil': 'BR',
            'uk': 'GB',
            'united kingdom': 'GB'
        }
        
        return country_codes.get(country.lower(), country.upper()[:2])

# Global instance
_geoshell = GeoShell()

# Convenience functions
def country(name: str, fields: Optional[List[str]] = None) -> CountryInfo:
    """Get country information"""
    return _geoshell.country(name, fields)

def weather(location: str, forecast: int = 0) -> WeatherInfo:
    """Get weather information"""
    return _geoshell.weather(location, forecast)

def holidays(country: str, year: Optional[int] = None) -> List[Holiday]:
    """Get national holidays"""
    return _geoshell.holidays(country, year)

def neighbors(country: str) -> List[str]:
    """Get neighboring countries"""
    return _geoshell.neighbors(country)

def timezone(location: str) -> Dict:
    """Get timezone information"""
    return _geoshell.timezone(location)

def news(country: str, limit: int = 10) -> List[Dict]:
    """Get latest news"""
    return _geoshell.news(country, limit)

# Example usage
if __name__ == "__main__":
    print("GeoShell Core Library")
    print("====================")
    
    # Test country function
    try:
        japan = country("Japan")
        print(f"\nCountry: {japan.name}")
        print(f"Capital: {japan.capital}")
        print(f"Population: {japan.population:,}")
        print(f"Region: {japan.region}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test weather function
    try:
        tokyo_weather = weather("Tokyo")
        print(f"\nWeather in {tokyo_weather.location}:")
        print(f"Temperature: {tokyo_weather.temperature}°C")
        print(f"Condition: {tokyo_weather.condition}")
        print(f"Humidity: {tokyo_weather.humidity}%")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test neighbors function
    try:
        german_neighbors = neighbors("Germany")
        print(f"\nGermany's neighbors: {', '.join(german_neighbors)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nGeoShell core library loaded successfully!")
