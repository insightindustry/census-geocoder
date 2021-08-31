"""
*****************************
tests/test_MatchedAddress
*****************************

Tests for the :class:`MatchedAddress`-related classes.

"""

import pytest
from tests.fixtures import input_files

from census_geocoder.locations import MatchedAddress
from census_geocoder import constants, errors


@pytest.mark.parametrize('kwargs, error', [
    ({}, None),
    ({
        "result": {
            "matchedAddress": "4600 SILVER HILL RD, WASHINGTON, DC, 20233",
            "coordinates": {
                "x": -76.92744,
                "y": 38.845985
            },
            "tigerLine": {
                "tigerLineId": "76355984",
                "side": "L"
            },
            "addressComponents": {
    			"fromAddress": "4600",
    			"toAddress": "4700",
    			"preQualifier": "",
    			"preDirection": "",
    			"preType": "",
    			"streetName": "SILVER HILL",
    			"suffixType": "RD",
    			"suffixDirection": "",
    			"suffixQualifier": "",
    			"city": "WASHINGTON",
    			"state": "DC",
    			"zip": "20233"
    		}
        }
     }, None),

])
def test__init__(kwargs, error):
    if not error:
        result = MatchedAddress(**kwargs)
        assert result is not None
        assert isinstance(result, MatchedAddress) is True

        assert kwargs.get('matchedAddress') == result.address
        assert kwargs.get('coordinates', {}).get('x') == result.longitude
        assert kwargs.get('coordinates', {}).get('y') == result.latitude
    else:
        with pytest.raises(error):
            result = MatchedAddress(**kwargs)
