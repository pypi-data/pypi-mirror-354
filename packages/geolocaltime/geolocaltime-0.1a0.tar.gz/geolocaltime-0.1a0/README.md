# geolocaltime-py
Accurately enriches location data with local time and time-of-day insights.

This modern Python module represents an idiomatic client accessing the [Geolocaltime location services](https://geospatial-ai.de/?rara-portfolio=geospatial-local-time-api-service) being hosted on [Rapid API Hub](https://v2.rapidapi.com/gisfromscratch/api/geolocaltime).

## Features

The geolocaltime API provides three main endpoints for geospatial time intelligence:

### 🌍 `/enrich` - Location Time Enrichment
Enriches locations with current local date and time values using standardized time zones. The local date and time value for each location are determined at the time of execution.

### 🔄 `/convert` - UTC to Local Time Conversion  
Converts date and time values from UTC to local time for specified locations using WGS84 coordinate system.

### 🕐 `/timeofday` - Time of Day Classification
Classifies local time values into meaningful time-of-day categories like "last night", "morning", "noon", "afternoon", "evening" and "night". The classifier uses seasonal locations of the sun and moon for realistic classifications.

## Key Capabilities

- **Batch Processing**: All endpoints support batch processing of up to 100 coordinates per request
- **Automatic Chunking**: Library automatically handles >100 coordinates by chunking requests
- **WGS84 Compatibility**: Uses WGS84 spatial reference system for precision and global compatibility
- **Comprehensive Validation**: Validates coordinate bounds and input consistency
- **Error Handling**: Robust error handling with descriptive messages

## Installation

```bash
pip install geolocaltime
```

## Quick Start

```python
from georapid.client import GeoRapidClient
from georapid.factory import EnvironmentClientFactory
from geolocaltime.services import enrich, convert, time_of_day
from geolocaltime.types import OutputType

# Set up client (requires RAPIDAPI_KEY environment variable)
host = 'geolocaltime.p.rapidapi.com'
client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)

# Define coordinates
latitudes = [50.0088, 39.437, 66.0557]
longitudes = [8.2756, -31.542, -23.7033]
utc_times = ['2024-10-19T09:18:42.542819'] * 3

# Enrich locations with current local time
enriched = enrich(client, latitudes, longitudes, OutputType.LOCAL)

# Convert UTC times to local times
converted = convert(client, latitudes, longitudes, utc_times, OutputType.LOCAL)

# Classify time of day
local_times = ['2025-06-09T21:58:01.010457+01:00', '2025-06-09T19:58:01.010457-01:00', '2025-06-09T20:58:01.010457+00:00']
time_classifications = time_of_day(client, latitudes, longitudes, local_times)
```

## Documentation

For detailed documentation, visit [geolocaltime.readthedocs.io](https://geolocaltime.readthedocs.io/en/latest).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
