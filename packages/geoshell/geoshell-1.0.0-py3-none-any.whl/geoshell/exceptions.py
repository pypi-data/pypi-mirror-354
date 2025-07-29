"""
GeoShell exceptions
"""

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