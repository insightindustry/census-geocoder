"""
*****************************
tests/test_GeographicArea
*****************************

Tests for the :class:`GeographicArea` class.

"""

import pytest
from tests.fixtures import input_files, check_input_file

from census_geocoder.geographies import GeographicArea
from census_geocoder.metaclasses import check_length
from census_geocoder import constants, errors


@pytest.mark.parametrize('as_dict, error', [
    ({}, None),
    ({
        "GEOID": "20746",
        "CENTLAT": "+38.8366493",
        "AREAWATER": 47839,
        "BASENAME": "20746",
        "OID": "221704257714982",
        "ZCTA5": "20746",
        "LSADC": "Z5",
        "FUNCSTAT": "S",
        "INTPTLAT": "+38.8364025",
        "NAME": "ZCTA5 20746",
        "OBJECTID": 1926,
        "CENTLON": "-076.9193615",
        "AREALAND": 19595655,
        "INTPTLON": "-076.9182650",
        "MTFCC": "G6350",
        "ZCTA5CC": "B5"
     }, None),
    ({
        "COUSUB": "90524",
        "GEOID": "2403390524",
        "CENTLAT": "+38.8406376",
        "AREAWATER": 64586,
        "STATE": "24",
        "BASENAME": "6, Spauldings",
        "OID": "27690286313747",
        "LSADC": "28",
        "FUNCSTAT": "N",
        "INTPTLAT": "+38.8404712",
        "NAME": "District 6, Spauldings",
        "OBJECTID": 3899,
        "CENTLON": "-076.9085553",
        "COUSUBCC": "Z1",
        "AREALAND": 55544427,
        "INTPTLON": "-076.9057059",
        "MTFCC": "G4040",
        "COUSUBNS": "01929662",
        "COUNTY": "033"
     }, None),

])
def test_from_dict(as_dict, error):
    if not error:
        result = GeographicArea.from_dict(as_dict)
        assert result is not None
        assert isinstance(result, GeographicArea) is True

    else:
        with pytest.raises(error):
            result = GeographicArea.from_dict(as_dict)


@pytest.mark.parametrize('kwargs, error', [
    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223'
    }, None),
    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'Current'
    }, None),
    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'current'
    }, None),
    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'CENSUS2020'
    }, errors.UnrecognizedVintageError),
    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'CENSUS2020',
        'vintage': 'Census2020'
    }, None),

    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'current',
        'vintage': 'census2020'
    }, None),
    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'census2020',
        'vintage': 'census2020'
    }, None),

    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'current',
        'vintage': 'census2020',
        'layers': 'urban growth areas, blocks, divisions, census regions'
    }, None),

    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'CENSUS2020',
        'vintage': 'does-not-exist'
    }, errors.UnrecognizedVintageError),
    ({
        'one_line': '4600 Silver Hill Rd, Washington, DC 20223',
        'benchmark': 'CENSUS2020',
        'vintage': 'ACS2019'
    }, errors.UnrecognizedVintageError),


    ({
        'street_1': '4600 Silver Hill Rd',
        'city': 'Washington',
        'state': 'DC',
        'zip_code': '20223'
    }, None),
    ({
        'city': 'Washington',
        'state': 'DC',
        'zip_code': '20223'
    }, errors.CensusAPIError),

    ({}, errors.NoAddressError),
])
def test_from_address(kwargs, error):
    if not error:
        result = GeographicArea.from_address(**kwargs)
        assert result is not None
        assert isinstance(result, GeographicArea) is True
    else:
        with pytest.raises(error):
            result = GeographicArea.from_address(**kwargs)


@pytest.mark.parametrize('args, kwargs, error', [
    (None, None, errors.NoAddressError),
    ([-76.92744, 38.845985], None, None),
    (None, {
        'longitude': -76.92744,
        'latitude': 38.845985
    }, None),
])
def test_from_coordinates(args, kwargs, error):
    if not error and args:
        result = GeographicArea.from_coordinates(*args)
    elif not error and kwargs:
        result = GeographicArea.from_coordinates(**kwargs)
    elif error and args:
        with pytest.raises(error):
            result = GeographicArea.from_coordinates(*args)
    elif error and kwargs:
        with pytest.raises(error):
            result = GeographicArea.from_coordinates(**kwargs)

    if not error:
        assert result is not None
        assert isinstance(result, GeographicArea) is True


@pytest.mark.parametrize('input_value, kwargs, error', [
    ('successful_batch.csv', {}, None),
    ('successful_batch.csv', { 'layers': 'all' }, None),
    ('error_batch.csv', {}, errors.MalformedBatchFileError),
])
def test_from_batch(input_files, input_value, kwargs, error):
    input_value = check_input_file(input_files, input_value)

    file_length = check_length(input_value)

    kwargs['file_'] = input_value

    if not error:
        result = GeographicArea.from_batch(**kwargs)
        assert result is not None
        assert isinstance(result, list) is True
        assert len(result) == file_length
        for item in result:
            assert isinstance(item, GeographicArea) is True
    else:
        with pytest.raises(error):
            result = GeographicArea.from_batch(**kwargs)
