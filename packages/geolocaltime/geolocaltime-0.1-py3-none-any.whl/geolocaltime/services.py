# author: Jan Tschada
# SPDX-License-Identifier: Apache-2.0

from georapid.client import GeoRapidClient
import requests
from typing import List
from .types import OutputType


def _chunk_coordinates(latitudes: List[float], longitudes: List[float], times: List[str] = None, chunk_size: int = 100):
    """
    Chunks coordinate lists into batches of specified size for API processing.
    
    :param latitudes: List of latitude values
    :param longitudes: List of longitude values  
    :param times: Optional list of time values
    :param chunk_size: Maximum size per chunk (default 100)
    :return: Generator yielding tuples of (lat_chunk, lon_chunk, time_chunk)
    """
    for i in range(0, len(latitudes), chunk_size):
        end_idx = min(i + chunk_size, len(latitudes))
        lat_chunk = latitudes[i:end_idx]
        lon_chunk = longitudes[i:end_idx]
        time_chunk = times[i:end_idx] if times is not None else None
        yield lat_chunk, lon_chunk, time_chunk


def enrich(client: GeoRapidClient, latitudes: List[float], longitudes: List[float], out: OutputType = OutputType.LOCAL) -> List[str]:
    """
    Enriches locations using date and time values of the corresponding standard time zones. 
    The local date and time value for each location are determined at the time of execution.

    :param client: The client instance to use for this query.
    :param latitudes: The latitudes representing the locations.
    :param longitudes: The longitudes representing the locations.
    :param out: The output for the timestamps e.g. "local" means local time or "dtc" means date-time-classification.

    :return: A list of date and time values for each location.
    """
    # Validate input parameters
    if len(latitudes) != len(longitudes):
        raise ValueError("latitudes and longitudes must have the same length.")
    
    # Handle empty inputs
    if len(latitudes) == 0:
        return []
    
    for latitude in latitudes:
        if latitude < -90.0 or 90.0 < latitude:
            raise ValueError(f'Invalid latitude value! {latitude} is not in the range of [-90.0, 90.0].')

    for longitude in longitudes:
        if longitude < -180.0 or 180.0 < longitude:
            raise ValueError(f'Invalid longitude value! {longitude} is not in the range of [-180.0, 180.0].')

    # Process in chunks to handle batch limits
    all_results = []
    for lat_chunk, lon_chunk, _ in _chunk_coordinates(latitudes, longitudes):
        # Prepare the request payload for this chunk
        payload = {
            'lat': lat_chunk,
            'lon': lon_chunk,
            'out': out.value
        }

        # Make the request to the service
        endpoint = '{0}/enrich'.format(client.url)
        response = requests.post(endpoint, headers=client.auth_headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        # Collect results from this chunk
        chunk_results = response.json()
        all_results.extend(chunk_results)

    return all_results

def convert(client: GeoRapidClient, latitudes: List[float], longitudes: List[float], times: List[str], out: OutputType = OutputType.LOCAL) -> List[str]:
    """
    Converts date and time values from UTC to local time or time of day for the specified locations.

    :param client: The client instance to use for this query.
    :param latitudes: The latitudes representing the locations.
    :param longitudes: The longitudes representing the locations.
    :param times: The UTC times for each location in ISO 8601 format.
    :param out: The output for the timestamps e.g. "local" means local time or "dtc" means date-time-classification.

    :return: A list of date and time values for each location.
    """
    # Validate input parameters
    if len(latitudes) != len(longitudes) or len(latitudes) != len(times):
        raise ValueError("latitudes, longitudes, and times must have the same length.")
    
    # Handle empty inputs
    if len(latitudes) == 0:
        return []
    
    for latitude in latitudes:
        if latitude < -90.0 or 90.0 < latitude:
            raise ValueError(f'Invalid latitude value! {latitude} is not in the range of [-90.0, 90.0].')

    for longitude in longitudes:
        if longitude < -180.0 or 180.0 < longitude:
            raise ValueError(f'Invalid longitude value! {longitude} is not in the range of [-180.0, 180.0].')

    # Process in chunks to handle batch limits
    all_results = []
    for lat_chunk, lon_chunk, time_chunk in _chunk_coordinates(latitudes, longitudes, times):
        # Prepare the request payload for this chunk
        payload = {
            'lat': lat_chunk,
            'lon': lon_chunk,
            'time': time_chunk,
            'out': out.value
        }

        # Make the request to the service
        endpoint = '{0}/convert'.format(client.url)
        response = requests.post(endpoint, headers=client.auth_headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        # Collect results from this chunk
        chunk_results = response.json()
        all_results.extend(chunk_results)

    return all_results

def time_of_day(client: GeoRapidClient, latitudes: List[float], longitudes: List[float], times: List[str]) -> List[str]:
    """
    Classifies local time values to time of day values like „last night“, „morning“, „noon“, „afternoon“, „evening“ and „night“.
    The classifier uses seasonal locations of the sun and moon providing realistic classifications.

    :param client: The client instance to use for this query.
    :param latitudes: The latitudes representing the locations.
    :param longitudes: The longitudes representing the locations.
    :param times: The UTC times for each location in ISO 8601 format.

    :return: A list of time of day values for each location.
    """
    # Validate input parameters
    if len(latitudes) != len(longitudes) or len(latitudes) != len(times):
        raise ValueError("latitudes, longitudes, and times must have the same length.")
    
    # Handle empty inputs
    if len(latitudes) == 0:
        return []
    
    for latitude in latitudes:
        if latitude < -90.0 or 90.0 < latitude:
            raise ValueError(f'Invalid latitude value! {latitude} is not in the range of [-90.0, 90.0].')

    for longitude in longitudes:
        if longitude < -180.0 or 180.0 < longitude:
            raise ValueError(f'Invalid longitude value! {longitude} is not in the range of [-180.0, 180.0].')

    # Process in chunks to handle batch limits
    all_results = []
    for lat_chunk, lon_chunk, time_chunk in _chunk_coordinates(latitudes, longitudes, times):
        # Prepare the request payload for this chunk
        payload = {
            'lat': lat_chunk,
            'lon': lon_chunk,
            'time': time_chunk
        }

        # Make the request to the service
        endpoint = '{0}/timeofday'.format(client.url)
        response = requests.post(endpoint, headers=client.auth_headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        # Collect results from this chunk
        chunk_results = response.json()
        all_results.extend(chunk_results)

    return all_results
