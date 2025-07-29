Geospatial Local Time API Service
=================================
Accurately enriches location data with local time and time-of-day insights.

This modern Python module represents an idiomatic client accessing the `Geolocaltime location services <https://geospatial-ai.de/?rara-portfolio=geospatial-local-time-api-service>`__ being hosted on `Rapid API Hub <https://v2.rapidapi.com/gisfromscratch/api/geolocaltime>`__.

Our Geospatial Local Time API transforms latitude and longitude coordinates into meaningful local time information using standardized time zones. This service leverages the WGS84 spatial reference system, ensuring precision and compatibility with global geospatial data.

API Endpoints
-------------

The geolocaltime service offers three powerful endpoints:

**🌍 /enrich** - Location Time Enrichment
   Enriches locations using date and time values of the corresponding standard time zones. The local date and time value for each location are determined at the time of execution.

**🔄 /convert** - UTC to Local Time Conversion
   Converts date and time values from UTC to local time for the specified locations.

**🕐 /timeofday** - Time of Day Classification
   Classifies local time values to time of day values like "last night", "morning", "noon", "afternoon", "evening" and "night". The classifier uses seasonal locations of the sun and moon providing realistic classifications.

Key Features
------------

* **Batch Processing**: All API endpoints support batch processing of up to 100 coordinates per request
* **Automatic Chunking**: The Python library automatically handles larger datasets by chunking requests
* **WGS84 Compatibility**: Uses the WGS84 spatial reference system for global precision
* **Comprehensive Validation**: Input validation for coordinate bounds and array consistency
* **Robust Error Handling**: Descriptive error messages for troubleshooting

Why is it important?
--------------------

Geospatial intelligence services enrich locations into standard time zones, enabling accurate temporal analysis across global datasets. Each location is represented by coordinate pairs using WGS84 as the spatial reference standard.

Next steps
----------
Please, check out the `RapidAPI Account Creation and Management Guide <https://docs.rapidapi.com/docs/account-creation-and-settings>`__.

Start with the :doc:`usage` section for further information, including
how to :ref:`installation` the Python module.

.. note::

   This project is under active development.

Contents
--------

.. toctree::

   usage
   api
