"""
Command-line interface for GeoShell
"""

import argparse
import json
import sys
from . import core

def main():
    parser = argparse.ArgumentParser(description="GeoShell - Real-time geo-data from your terminal")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Country command
    country_parser = subparsers.add_parser("country", help="Get country information")
    country_parser.add_argument("name", help="Country name or ISO code")
    country_parser.add_argument("--fields", help="Comma-separated list of fields to include")
    
    # Weather command
    weather_parser = subparsers.add_parser("weather", help="Get weather data")
    weather_parser.add_argument("location", help="City name or coordinates")
    weather_parser.add_argument("--forecast", type=int, help="Number of forecast days (0-7)")
    
    # Holidays command
    holidays_parser = subparsers.add_parser("holidays", help="Get national holidays")
    holidays_parser.add_argument("country", help="Country name or ISO code")
    holidays_parser.add_argument("--year", type=int, help="Year to get holidays for")
    holidays_parser.add_argument("--upcoming", action="store_true", help="Show only upcoming holidays")
    
    # Neighbors command
    neighbors_parser = subparsers.add_parser("neighbors", help="Get neighboring countries")
    neighbors_parser.add_argument("country", help="Country name or ISO code")
    
    # Global options
    parser.add_argument("--format", choices=["json", "table", "csv"], default="json", help="Output format")
    parser.add_argument("--output", help="Save output to file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        result = None
        
        if args.command == "country":
            fields = args.fields.split(",") if args.fields else None
            result = core.country(args.name, fields)
            if hasattr(result, "to_dict"):
                result = result.to_dict()
        
        elif args.command == "weather":
            result = core.weather(args.location, args.forecast or 0)
            if hasattr(result, "to_dict"):
                result = result.to_dict()
        
        elif args.command == "holidays":
            result = core.holidays(args.country, args.year)
            if hasattr(result, "to_dict"):
                result = [h.to_dict() for h in result]
        
        elif args.command == "neighbors":
            result = core.neighbors(args.country)
        
        # Format output
        output = format_output(result, args.format)
        
        # Save or print output
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Output saved to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def format_output(data, format_type):
    if format_type == "json":
        return json.dumps(data, indent=2)
    elif format_type == "table":
        # Implement table formatting
        pass
    elif format_type == "csv":
        # Implement CSV formatting
        pass
    return str(data)

if __name__ == "__main__":
    main()