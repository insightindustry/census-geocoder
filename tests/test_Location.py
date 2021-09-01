"""
***********************
tests/test_Location
***********************

Tests for the :class:`Location`-related classes.

"""

import pytest
from tests.fixtures import input_files, check_input_file

from census_geocoder.locations import Location, MatchedAddress
from census_geocoder.metaclasses import check_length
from census_geocoder import constants, errors


@pytest.mark.parametrize('kwargs, error', [
    ({}, None),
    ({
        'input_one_line': '4600 Silver Hill Rd, Washington, DC, 20233'
    }, None),
    ({
        'input_street': '4600 Silver Hill Rd',
        'input_city': 'Washington',
        'input_state': 'DC',
        'input_zip_code': '20233'
    }, None),
    ({
        'benchmark_name': 'Public_AR_Current'
    }, None),
    ({
        'benchmark_name': 'Public_AR_Current',
        'vintage_name': 'Current_Current'
    }, None),
])
def test__init__(kwargs, error):
    if not error:
        result = Location(**kwargs)
        assert result is not None
        assert isinstance(result, Location) is True

        for key in kwargs:
            assert getattr(result, key) == kwargs.get(key)
            if key == 'benchmark_name':
                for benchmark_key in constants.BENCHMARKS:
                    if constants.BENCHMARKS.get(benchmark_key) == kwargs.get(key):
                        assert result.benchmark == benchmark_key
            if key == 'vintage_name' and result.benchmark is not None:
                vintage_set = constants.VINTAGES.get(result.benchmark_name)
                for vintage_key in vintage_set:
                    if result.vintage_name == vintage_set.get(vintage_key):
                        assert result.vintage == vintage_key
    else:
        with pytest.raises(error):
            result = Location(**kwargs)


@pytest.mark.parametrize('kwargs, error', [
    ({}, None),
    ({
        'input_one_line': '4600 Silver Hill Rd, Washington, DC, 20233'
    }, None),
    ({
        'input_street': '4600 Silver Hill Rd',
        'input_city': 'Washington',
        'input_state': 'DC',
        'input_zip_code': '20233'
    }, None),
    ({
        'benchmark_name': 'Public_AR_Current'
    }, None),
    ({
        'benchmark_name': 'Public_AR_Current',
        'vintage_name': 'Current_Current'
    }, None),
])
def test_inspect(kwargs, error):
    if not error:
        obj = Location(**kwargs)
        values = 0
        for key in kwargs:
            values += 1

        result = obj.inspect()
        assert result is not None
        assert isinstance(result, list) is True
        assert len(result) >= values

        as_census_result = obj.inspect(as_census_fields = True)
        assert as_census_result is not None
        assert isinstance(as_census_result, list) is True
        assert len(as_census_result) >= values
    else:
        obj = Location(**kwargs)
        with pytest.raises(error):
            result = obj.inspect()


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
        'vintage': 'CENSUS2020'
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
        result = Location.from_address(**kwargs)
        assert result is not None
        assert isinstance(result, Location) is True
        assert result.matched_addresses is not None
        assert len(result.matched_addresses) > 0
    else:
        with pytest.raises(error):
            result = Location.from_address(**kwargs)


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
        result = Location.from_coordinates(*args)
    elif not error and kwargs:
        result = Location.from_coordinates(**kwargs)
    elif error and args:
        with pytest.raises(error):
            result = Location.from_coordinates(*args)
    elif error and kwargs:
        with pytest.raises(error):
            result = Location.from_coordinates(**kwargs)

    if not error:
        assert result is not None
        assert isinstance(result, Location) is True
        assert result.geographies is not None
        assert len(result.geographies) > 0


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
        result = Location.from_batch(**kwargs)
        assert result is not None
        assert isinstance(result, list) is True
        assert len(result) == file_length
        for item in result:
            assert isinstance(item, Location) is True
    else:
        with pytest.raises(error):
            result = Location.from_batch(**kwargs)
