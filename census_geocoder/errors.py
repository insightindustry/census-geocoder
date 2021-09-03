# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member class documentation is automatically incorporated
# there as needed.

import warnings
from validator_collection import validators


class CensusGeocoderError(ValueError):
    """Base error raised by the **Census Geocoder**. Inherits from
    :class:`ValueError <python:ValueError>`.
    """
    pass


class CensusGeocoderWarning(UserWarning):
    """Base warning raised by the **Census Geocoder**. Inherits from
    :class:`UserWarning <python:warnings.UserWarning>`."""
    pass


class CensusAPIError(CensusGeocoderError):
    """Error raised when the `Census Geocoder API`_ returned an error."""
    pass


class ConfigurationError(CensusGeocoderError):
    """Error raised when a geocoding request was configured incorrectly."""
    pass


class UnrecognizedBenchmarkError(ConfigurationError):
    """Error raised when a :term:`benchmark` has been specified incorrectly."""
    pass


class UnrecognizedVintageError(ConfigurationError):
    """Error raised when a :term:`vintage` has been specified incorrectly."""
    pass


class MalformedBatchFileError(ConfigurationError):
    """Error raised when a batch file is structured improperly."""
    pass


class NoAddressError(ConfigurationError):
    """Error raised when there was no address supplied with the request."""
    pass


class BatchSizeTooLargeError(ConfigurationError):
    """Error raised when the size of a batch address file exceeds the limit of 10,000
    imposed by the `Census Geocoder API`_."""
    pass


class NoFileProvidedError(ConfigurationError):
    """Error raised when a batch file indicated in the request does not exist or cannot
    be read."""
    pass


class EntityNotFoundError(CensusGeocoderError):
    """Error raised when a matching geographic entity could not be identified. Inherits
    from :class:`CensusGeocoderError`.
    """

    @staticmethod
    def evaluate(result, request_type = None):
        """Returns ``True`` if the `Census Geocoder API`_ was unable to match a geographic
        entity to the request. Returns ``False`` if the API was able to match
        successfully.

        :param result: The response from the `Census Geocoder API`_.
        :type result: :class:`requests.Response <requests:Response>`

        :param request_type: The classificaiton of the geocoding request. Indicates what
          type of data is to be returned, which determines how the result is evaluated.
          Expects either ``'geographies'`` or ``'locations'``.
        :type request_type: :class:`str <python:str>`

        :returns: ``True`` if geocoding was successful. ``False`` if not.
        :rtype: :class:`bool <python:bool>`
        """
        if result.status_code == 404:
            return True

        if result.text == '{}':
            return True

        as_dict = validators.dict(result.json())

        if request_type == 'locations':
            matched_addresses = as_dict.get('result', {}).get('addressMatches', [])
            if not matched_addresses:
                return True

        if request_type == 'geographies':
            matched_addresses = as_dict.get('result', {}).get('addressMatches', [])
            geographies = as_dict.get('result', {}).get('geographies', [])
            if matched_addresses and not geographies:
                return False
            elif not geographies:
                return True

        return False
