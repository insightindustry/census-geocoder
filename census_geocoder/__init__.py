# -*- coding: utf-8 -*-
"""(Unofficial) Python bindings for the US Census Geocoder API.

While this entry point to the library exposes all classes and functions for
convenience, those items themselves are actually implemented and documented in
child modules.
"""

import os
from census_geocoder import locations, geographies, errors

# Get the version number from the _version.py file
version_dict = {}

with open(os.path.join(os.path.dirname(__file__), '__version__.py')) as version_file:
    exec(version_file.read(), version_dict)

__version__ = version_dict.get('__version__')

location = locations.Location
geography = geographies.GeographicArea
geography_collection = geographies.GeographyCollection
matched_address = locations.MatchedAddress

__all__ = [
    'location',
    'geography',
    'geography_collection',
    'matched_address',
    'errors'
]
