**********************************
Error Reference
**********************************

.. module:: census_geocoder.errors

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

Handling Errors
=================

Stack Traces
--------------

Because the **Census Geocoder** produces exceptions which inherit from the
standard library, it leverages the same API for handling stack trace information.
This means that it will be handled just like a normal exception in unit test
frameworks, logging solutions, and other tools that might need that information.

------------------

Census Geocoder Errors
==========================

CensusGeocoderError (from :class:`ValueError <python:ValueError>`)
--------------------------------------------------------------------

.. autoclass:: CensusGeocoderError

----------------

CensusAPIError (from :class:`CensusGeocoderError`)
--------------------------------------------------------------------

.. autoclass:: CensusAPIError

----------------

ConfigurationError (from :class:`CensusGeocoderError`)
--------------------------------------------------------------------

.. autoclass:: ConfigurationError

----------------

UnrecognizedBenchmarkError (from :class:`ConfigurationError`)
----------------------------------------------------------------

.. autoclass:: UnrecognizedBenchmarkError

----------------

UnrecognizedVintageError (from :class:`ConfigurationError`)
----------------------------------------------------------------

.. autoclass:: UnrecognizedVintageError

----------------

MalformedBatchFileError (from :class:`ConfigurationError`)
----------------------------------------------------------------

.. autoclass:: MalformedBatchFileError

----------------

NoAddressError (from :class:`ConfigurationError`)
----------------------------------------------------------------

.. autoclass:: NoAddressError

----------------

NoFileProvidedError (from :class:`ConfigurationError`)
----------------------------------------------------------------

.. autoclass:: NoFileProvidedError

----------------

BatchSizeTooLargeError (from :class:`ConfigurationError`)
----------------------------------------------------------------

.. autoclass:: BatchSizeTooLargeError

----------------

Census Geocoder Warnings
===========================

CensusGeocoderWarning (from :class:`UserWarning <python:UserWarning>`)
------------------------------------------------------------------------

.. autoclass:: CensusGeocoderWarning

.. _Census Geocoder API: https://geocoding.geo.census.gov/geocoder/
