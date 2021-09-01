# -*- coding: utf-8 -*-

# The lack of a module docstring for this module is **INTENTIONAL**.
# The module is imported into the documentation using Sphinx's autodoc
# extension, and its member class documentation is automatically incorporated
# there as needed.

import warnings


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
