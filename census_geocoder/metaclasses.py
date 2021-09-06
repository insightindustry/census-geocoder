"""
###################################
census_geocoder/metaclasses.py
###################################

Defines the metaclasses that are used throughout the library.

"""
import os
from abc import ABC, abstractmethod
import csv
import json

import requests
from validator_collection import validators
from backoff_utils import backoff

from census_geocoder import errors
from census_geocoder.constants import CENSUS_API_URL, BENCHMARKS, VINTAGES, LAYERS

DEFAULT_BENCHMARK = os.environ.get('CENSUS_GEOCODER_BENCHMARK', 'CURRENT')
DEFAULT_VINTAGE = os.environ.get('CENSUS_GEOCODER_VINTAGE', 'CURRENT')
DEFAULT_LAYERS = os.environ.get('CENSUS_GEOCODER_LAYERS', 'all')


def parse_benchmark_vintage_layers(benchmark = DEFAULT_BENCHMARK,
                                   vintage = DEFAULT_VINTAGE,
                                   layers = DEFAULT_LAYERS):
    """Parse the benchmark and vintage received.

    :param benchmark: The :term:`Benchmark` value to parse into its canonical form.
      Defaults to ``CURRENT`` unless overridden by the ``CENSUS_GEOCODER_BENCHMARK``
      environment variable.
    :type benchmark: :class:`str <python:str>`

    :param vintage: The :term:`Vintage` value to parse into its canonical form.
      Defaults to ``CURRENT`` unless overridden by the ``CENSUS_GEOCODER_VINTAGE``
      environment variable.
    :type vintage: :class:`str <python:str>`

    :param layers: The :term:`Layers <Layer>` that should be parsed into its canonical
      form. Defaults to ``all`` unless overridden by the ``CENSUS_GEOCODER_LAYERS``
      environment variable.
    :type layers: :class:`str <python:str>`

    :returns: The canonical ``(benchmark, vintage, layers)``.
    :rtype: :class:`tuple <python:tuple>` of :class:`str <python:str>`,
      :class:`str <python:str>`, and :class:`str <python:str>`

    :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
      recognized
    :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized within
      the ``benchmark`` specified

    """
    target_benchmark = validators.string(benchmark, allow_empty = False).upper()
    benchmark = BENCHMARKS.get(target_benchmark, None)
    if not benchmark:
        raise errors.UnrecognizedBenchmarkError(
            f'Benchmark ({target_benchmark}) is not a recognized benchmark.'
        )

    possible_vintages = VINTAGES.get(benchmark, None)
    target_vintage = validators.string(vintage, allow_empty = False).upper()
    vintage = possible_vintages.get(target_vintage, None)
    if not vintage:
        raise errors.UnrecognizedVintageError(
            f'Vintage ({target_vintage}) is not a recognized/available vintage within the'
            f' "{benchmark}" benchmark.'
        )

    if layers != 'all':
        layer_set = LAYERS.get(vintage, None)
        if layer_set:
            layer_set_lowercase = {}
            for key in layer_set:
                layer_set_lowercase[key.lower()] = layer_set.get(key)

            layer_targets = layers.split(',')
            layer_targets = [x.strip() for x in layer_targets]

            layers = []
            for layer in layer_targets:
                layer_lower = layer.lower()
                if layer_lower in layer_set_lowercase:
                    layers.append(str(layer_set_lowercase.get(layer_lower, None)))

            layers = ','.join(layers)
        else:
            layers = None

    return benchmark, vintage, layers


def check_length(file_):
    """Returns the number of records in the indicated file.

    :param file_: The filename of the file to check. Expects a CSV or TXT file.
    :type file_: :class:`str <python:str>`

    :returns: The number of records in the indicated file.
    :rtype: :class:`int <python:int>`

    """
    file_ = validators.file_exists(file_, allow_empty = False)
    with open(file_, 'r') as file_object:
        csv_reader = csv.reader(file_object)
        row_count = sum(1 for row in csv_reader)

    return row_count


class BaseEntity(ABC):
    """Abstract base clase for geographic entities that may or may not be supported by the
    API."""

    @property
    @abstractmethod
    def entity_type(self):
        """The type of geographic entity that the object represents. Supports either:
        ``locations`` or ``geographies``.

        :rtype: :class:`str <python:str>`
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_dict(cls, as_dict):
        """Create an instance of the geographic entity from its
        :class:`dict <python:dict>` representation.

        :param as_dict: The :class:`dict <python:dict>` representation of the geographic
          entity.
        :type as_dict: :class:`dict <python:dict>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`GeographicEntity`

        """
        raise NotImplementedError()

    @classmethod
    def from_json(cls, as_json):
        """Create an instance of the geographic entity from its JSON representation.

        :param as_json: The JSON representation of the geographic entity.
        :type as_json: :class:`str <python:str>`, :class:`dict <python:dict>`, or
          :class:`list <python:list>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`GeographicEntity`

        """
        as_dict = validators.json(as_json, allow_empty = False)

        return cls.from_dict(as_dict)

    @classmethod
    @abstractmethod
    def from_csv_record(cls, csv_record):
        """Create an instance of the geographic entity from its CSV record.

        :param csv_record: The list of columns for the CSV record.
        :type csv_record: :class:`list <python:list>` of :class:`str <python:str>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`GeographicEntity`

        """
        raise NotImplementedError()

    @abstractmethod
    def to_dict(self):
        """Returns a :class:`dict <python:dict>` representation of the geographic entity.

        .. note::

          The :class:`dict <python:dict>` representation matches the JSON structure for
          the US Census Geocoder API. This is a not-very-pythonic
          :class:`dict <python:dict>` structure, but at least this ensures idempotency.

        :returns: :class:`dict <python:dict>` representation of the entity.
        :rtype: :class:`dict <python:dict>`
        """
        raise NotImplementedError()

    def to_json(self):
        """Returns a JSON representation of the geographic entity.

        .. note::

          The JSON representation matches the JSON structure for
          the US Census Geocoder API. This is a not-very-pythonic
          structure, but at least this ensures idempotency.

        :returns: :class:`str <python:str>` representation of the entity.
        :rtype: :class:`str <python:str>`
        """
        as_dict = self.to_dict()
        return json.dumps(as_dict)


class GeographicEntity(BaseEntity):
    """Abstract base class for geographic entities that *are* supported by the API.
    """

    @classmethod
    def _get_one_line(cls,
                      one_line,
                      benchmark = DEFAULT_BENCHMARK,
                      vintage = DEFAULT_VINTAGE,
                      layers = DEFAULT_LAYERS):
        """Return data from a single-line address.

        :param one_line: The one-line address to geocode.
        :type one_line: :class:`str <python:str>`

        :param benchmark: The name of the :term:`benchmark` of data to return. The default
          value is determined by the ``CENSUS_GEOCODER_BENCHMARK`` environment variable,
          and if that is not set defaults to ``'Current'`` which represents the current
          default benchmark, per the `Census Geocoder API`_.

          Accepts the following values:

            * ``'Current'`` (default)
            * ``'Census2020'``

        :type benchmark: :class:`str <python:str>`

        :param vintage: The vintage of Census data for which data should be returned. The
          default value is determined by the ``CENSUS_GEOCODER_VINTAGE`` environment
          variable, and if that is not set defaults to ``'Current'`` which represents the
          default vintage per the `Census Geocoder API`_.

          Acceptable values are dependent on the ``benchmark`` specified, as per the table below:

            +--------------+---------------------+---------------------+
            |              |                 BENCHMARKS                |
            +              +---------------------+---------------------+
            |              | Current             | Census2020          |
            +==============+=====================+=====================+
            | **VINTAGES** | Current             | Census2020          |
            +              +---------------------+---------------------+
            |              | Census2020          | Census2010          |
            +              +---------------------+---------------------+
            |              | ACS2019             |                     |
            +              +---------------------+---------------------+
            |              | ACS2018             |                     |
            +              +---------------------+---------------------+
            |              | ACS2017             |                     |
            +              +---------------------+---------------------+
            |              | Census2010          |                     |
            +--------------+---------------------+---------------------+

        :type vintage: :class:`str <python:str>`

        :param layers: The set of geographic layers to return for the request. The default
          value is determined by the ``CENSUS_GEOCODER_LAYERS`` environment variable, and
          if that is not set defaults to ``'all'``.

            .. seealso::

              * :doc:`Geographies <geographies>` :ref:`Benchmarks, Vintages, and Layers <benchmarks_vintages_and_layers>`

        :type layers: :class:`str <python:str>`

        :rtype: :class:`dict <python:dict>`

        :raises CensusAPIError: if the Census Geocoder API returned an error
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        one_line = validators.string(one_line)
        benchmark, vintage, layers = parse_benchmark_vintage_layers(benchmark,
                                                                    vintage,
                                                                    layers)

        parameters = {
            'address': one_line,
            'benchmark': benchmark,
            'vintage': vintage,
            'format': 'json'
        }
        if layers:
            parameters['layers'] = layers

        instance = cls()

        url = f'{CENSUS_API_URL}/geocoder/{instance.entity_type}/onelineaddress'

        result = backoff(requests.get,
                         args = [url],
                         kwargs = {'params': parameters},
                         max_tries = 5,
                         max_delay = 10)

        if 'Specify street' in result.text:
            raise errors.ConfigurationError(f'Did not provide a properly parametrized '
                                            'address.')
        elif errors.EntityNotFoundError.evaluate(result,
                                                 request_type = instance.entity_type):
            raise errors.EntityNotFoundError(
                f'Census Geocoder API was unable to find a matching geographic entity.'
            )
        elif result.status_code >= 400:
            raise errors.CensusAPIError(
                f'Census Geocoder API returned status code {result.status_code} with '
                f'message: "{result.text}".'
            )

        return result.json()

    @classmethod
    def _get_address(cls,
                     street_1 = None,
                     city = None,
                     state = None,
                     zip_code = None,
                     benchmark = DEFAULT_BENCHMARK,
                     vintage = DEFAULT_VINTAGE,
                     layers = DEFAULT_LAYERS):
        """Return data from a :term:`parametrized address`.

        :param street_1: A street address, e.g. ``'4600 Silver Hill Rd'``. Defaults to
          :obj:`None <python:None>`.
        :type street_1: :class:`str <python:str>` / :obj:`None <python:None>`

        :param street_2: A secondary component of a street address, e.g. ``'Floor 3'``.
          Defaults to :obj:`None <python:None>`.
        :type street_2: :class:`str <python:str>` / :obj:`None <python:None>`

        :param street_3: A tertiary component of a street address, e.g. ``'Apt. B'``.
          Defaults to :obj:`None <python:None>`.
        :type street_3: :class:`str <python:str>` / :obj:`None <python:None>`

        :param city: The city or town of a street address, e.g. ``'Washington'``.
          Defaults to :obj:`None <python:None>`.
        :type city: :class:`str <python:str>` / :obj:`None <python:None>`

        :param state: The state or territory of a street address, e.g. ``'DC'``.
          Defaults to :obj:`None <python:None>`.
        :type state: :class:`str <python:str>` / :obj:`None <python:None>`

        :param zip_code: The zip code (or zip code + 4) of a street address, e.g.
          ``'20233'``. Defaults to :obj:`None <python:None>`.
        :type zip_code: :class:`str <python:str>` / :obj:`None <python:None>`

        :param benchmark: The name of the :term:`benchmark` of data to return. The default
          value is determined by the ``CENSUS_GEOCODER_BENCHMARK`` environment variable,
          and if that is not set defaults to ``'Current'`` which represents the current
          default benchmark, per the `Census Geocoder API`_.

          Accepts the following values:

            * ``'Current'`` (default)
            * ``'Census2020'``

        :type benchmark: :class:`str <python:str>`

        :param vintage: The vintage of Census data for which data should be returned. The
          default value is determined by the ``CENSUS_GEOCODER_VINTAGE`` environment
          variable, and if that is not set defaults to ``'Current'`` which represents the
          default vintage per the `Census Geocoder API`_.

          Acceptable values are dependent on the ``benchmark`` specified, as per the table below:

            +--------------+---------------------+---------------------+
            |              |                 BENCHMARKS                |
            +              +---------------------+---------------------+
            |              | Current             | Census2020          |
            +==============+=====================+=====================+
            | **VINTAGES** | Current             | Census2020          |
            +              +---------------------+---------------------+
            |              | Census2020          | Census2010          |
            +              +---------------------+---------------------+
            |              | ACS2019             |                     |
            +              +---------------------+---------------------+
            |              | ACS2018             |                     |
            +              +---------------------+---------------------+
            |              | ACS2017             |                     |
            +              +---------------------+---------------------+
            |              | Census2010          |                     |
            +--------------+---------------------+---------------------+

        :type vintage: :class:`str <python:str>`

        :param layers: The set of geographic layers to return for the request. The default
          value is determined by the ``CENSUS_GEOCODER_LAYERS`` environment variable, and
          if that is not set defaults to ``'all'``.

            .. seealso::

              * :doc:`Geographies <geographies>` :ref:`Benchmarks, Vintages, and Layers <benchmarks_vintages_and_layers>`

        :type layers: :class:`str <python:str>`

        :rtype: :class:`dict <python:dict>`

        :raises NoAddressError: if the address information is completely empty
        :raises CensusAPIError: if the Census Geocoder API returned an error
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        street_1 = validators.string(street_1, allow_empty = True)
        city = validators.string(city, allow_empty = True)
        state = validators.string(state, allow_empty = True)
        zip_code = validators.string(zip_code, allow_empty = True)

        benchmark, vintage, layers = parse_benchmark_vintage_layers(benchmark,
                                                                    vintage,
                                                                    layers)

        parameters = {
            'benchmark': benchmark,
            'vintage': vintage,
            'format': 'json'
        }
        if layers:
            parameters['layers'] = layers

        is_valid = False
        if street_1:
            is_valid = True
            parameters['street'] = street_1
        if city:
            is_valid = True
            parameters['city'] = city
        if state:
            is_valid = True
            parameters['state'] = state
        if zip_code:
            is_valid = True
            parameters['zip'] = zip_code

        if not is_valid:
            raise errors.NoAddressError()

        instance = cls()

        url = f'{CENSUS_API_URL}/geocoder/{instance.entity_type}/address'

        result = backoff(requests.get,
                         args = [url],
                         kwargs = {'params': parameters},
                         max_tries = 5,
                         max_delay = 10)

        if 'Specify street' in result.text:
            raise errors.ConfigurationError(f'Did not provide a properly parametrized '
                                            f'address.')
        elif errors.EntityNotFoundError.evaluate(result,
                                                 request_type = instance.entity_type):
            raise errors.EntityNotFoundError(
                f'Census Geocoder API was unable to find a matching geographic entity.'
            )
        elif result.status_code >= 400:
            raise errors.CensusAPIError(
                f'Census Geocoder API returned status code {result.status_code} with '
                f'message: "{result.text}".'
            )

        return result.json()

    @classmethod
    def _get_batch_addresses(cls,
                             file_,
                             benchmark = DEFAULT_BENCHMARK,
                             vintage = DEFAULT_VINTAGE,
                             layers = DEFAULT_LAYERS):
        """Return data from a batch file in CSV, XLS/X, TXT, or DAT format.

        :param file_: The name of a file in CSV, XLS/X, DAT, or TXT format. Expects the
          file to have the following columns *without a header row*:

          * Unique ID
          * Street Address
          * City
          * State
          * Zip Code

        :type file_: :class:`str <python:str>`

        :param benchmark: The name of the :term:`benchmark` of data to return. Defaults to
          ``'Current'`` which represents the current default benchmark, per the Census
          Geocoder API. Accepts the following values:

          * ``'Current'`` (default)
          * ``'Census2020'``

        :type benchmark: :class:`str <python:str>`

        :param vintage: The vintage of Census data for which data should be returned.
          Defaults to ``'Current'`` which represents the current default vintage per the
          Census Geocoder API. Accepts the following values:

          * ``'Current'`` (default)
          * ``'Census2020'``
          * ``'ACS2019'``
          * ``'ACS2018'``
          * ``'ACS2017'``
          * ``'Census2010'``

        :type vintage: :class:`str <python:str>`

        :param layers: The set of geographic layers to return for the request. Defaults to
          ``'all'``.
        :type layers: :class:`str <python:str>`

        :rtype: :class:`list <python:list>` of :class:`GeographicEntity`

        :raises NoFileProvidedError: if no ``file_`` is provided
        :raises FileNotFoundError: if ``file_`` does not exist on the filesystem
        :raises BatchSizeTooLargeError: if ``file_`` contains more than 10,000 records

        :raises CensusAPIError: if the Census Geocoder API returned an error
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        benchmark, vintage, layers = parse_benchmark_vintage_layers(benchmark,
                                                                    vintage,
                                                                    layers)

        file_ = validators.file_exists(file_, allow_empty = False)
        file_length = check_length(file_)
        if file_length > 10000:
            raise errors.BatchSizeTooLargeError(f'Batch Too Large. Max of 10,000 entries '
                                                f'supported. File contains {file_length}')

        parameters = {
            'benchmark': benchmark,
            'vintage': vintage,
            'format': 'json'
        }
        if layers:
            parameters['layers'] = layers

        instance = cls()

        url = f'{CENSUS_API_URL}/geocoder/{instance.entity_type}/addressbatch'

        with open(file_, 'rb') as file_object:
            files = {
                'addressFile': (file_, file_object)
            }

            result = backoff(requests.post,
                             args = [url],
                             kwargs = {
                                 'files': files,
                                 'params': parameters
                             },
                             max_tries = 5,
                             max_delay = 10)

        if result.status_code >= 400 and 'Malformed input' in result.text:
            raise errors.MalformedBatchFileError('The batch file submitted did not have '
                                                 'the expected/required structure. Please'
                                                 ' check and resubmit.')
        elif result.status_code >= 400:
            raise errors.CensusAPIError(
                f'Census Geocoder API returned status code {result.status_code} with '
                f'message: "{result.text}".'
            )

        content = result.content.decode('utf-8')

        csv_reader = csv.reader(content.splitlines(), delimiter = ',')
        csv_list = list(csv_reader)

        return csv_list

    @classmethod
    def _get_coordinates(cls,
                         longitude,
                         latitude,
                         benchmark = DEFAULT_BENCHMARK,
                         vintage = DEFAULT_VINTAGE,
                         layers = DEFAULT_LAYERS):
        """Return data from a pair of geographic coordinates (longitude / latitude).

        :param longitude: The longitude coordinate.
        :type longitude: numeric

        :param latitude: The latitude coordinate.
        :type latitude: numeric

        :param benchmark: The name of the :term:`benchmark` of data to return. Defaults to
          ``'Current'`` which represents the current default benchmark, per the Census
          Geocoder API. Accepts the following values:

          * ``'Current'`` (default)
          * ``'Census2020'``

        :type benchmark: :class:`str <python:str>`

        :param vintage: The vintage of Census data for which data should be returned.
          Defaults to ``'Current'`` which represents the current default vintage per the
          Census Geocoder API. Accepts the following values:

          * ``'Current'`` (default)
          * ``'Census2020'``
          * ``'ACS2019'``
          * ``'ACS2018'``
          * ``'ACS2017'``
          * ``'Census2010'``

        :type vintage: :class:`str <python:str>`

        :param layers: The set of geographic layers to return for the request. Defaults to
          ``'all'``.
        :type layers: :class:`str <python:str>`

        :rtype: :class:`dict <python:dict>`

        :raises CensusAPIError: if the Census Geocoder API returned an error
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        longitude = validators.decimal(longitude, allow_empty = False)
        latitude = validators.decimal(latitude, allow_empty = False)

        benchmark, vintage, layers = parse_benchmark_vintage_layers(benchmark,
                                                                    vintage,
                                                                    layers)

        parameters = {
            'x': '{0:.6f}'.format(longitude),
            'y': '{0:.6f}'.format(latitude),
            'benchmark': benchmark,
            'vintage': vintage,
            'format': 'json'
        }
        if layers:
            parameters['layers'] = layers

        instance = cls()

        url = f'{CENSUS_API_URL}/geocoder/geographies/coordinates'

        result = backoff(requests.get,
                         args = [url],
                         kwargs = {'params': parameters},
                         max_tries = 5,
                         max_delay = 10)

        if errors.EntityNotFoundError.evaluate(result,
                                               request_type = 'geographies'):
            raise errors.EntityNotFoundError(
                f'Census Geocoder API was unable to find a matching geogrpahic entity.'
            )
        elif result.status_code >= 400:
            raise errors.CensusAPIError(
                f'Census Geocoder API returned status code {result.status_code} with '
                f'message: "{result.text}".'
            )

        return result.json()

    @classmethod
    def from_address(cls, *args, **kwargs):
        """Return data from an adddress, supplied either as a single
        :term:`one-line address` or a :term:`parametrized address`.

        :param one_line: A single-line address, e.g.
          ``'4600 Silver Hill Rd, Washington, DC 20233'``. Defaults to
          :obj:`None <python:None>`.
        :type one_line: :class:`str <python:str>` / :obj:`None <python:None>`

        :param street_1: A street address, e.g. ``'4600 Silver Hill Rd'``. Defaults to
          :obj:`None <python:None>`.
        :type street_1: :class:`str <python:str>` / :obj:`None <python:None>`

        :param street_2: A secondary component of a street address, e.g. ``'Floor 3'``.
          Defaults to :obj:`None <python:None>`.
        :type street_2: :class:`str <python:str>` / :obj:`None <python:None>`

        :param street_3: A tertiary component of a street address, e.g. ``'Apt. B'``.
          Defaults to :obj:`None <python:None>`.
        :type street_3: :class:`str <python:str>` / :obj:`None <python:None>`

        :param city: The city or town of a street address, e.g. ``'Washington'``.
          Defaults to :obj:`None <python:None>`.
        :type city: :class:`str <python:str>` / :obj:`None <python:None>`

        :param state: The state or territory of a street address, e.g. ``'DC'``.
          Defaults to :obj:`None <python:None>`.
        :type state: :class:`str <python:str>` / :obj:`None <python:None>`

        :param zip_code: The zip code (or zip code + 4) of a street address, e.g.
          ``'20233'``. Defaults to :obj:`None <python:None>`.
        :type zip_code: :class:`str <python:str>` / :obj:`None <python:None>`

        :param benchmark: The name of the :term:`benchmark` of data to return. The default
          value is determined by the ``CENSUS_GEOCODER_BENCHMARK`` environment variable,
          and if that is not set defaults to ``'Current'`` which represents the current
          default benchmark, per the `Census Geocoder API`_.

          Accepts the following values:

            * ``'Current'`` (default)
            * ``'Census2020'``

        :type benchmark: :class:`str <python:str>`

        :param vintage: The vintage of Census data for which data should be returned. The
          default value is determined by the ``CENSUS_GEOCODER_VINTAGE`` environment
          variable, and if that is not set defaults to ``'Current'`` which represents the
          default vintage per the `Census Geocoder API`_.

          Acceptable values are dependent on the ``benchmark`` specified, as per the table below:

            +--------------+---------------------+---------------------+
            |              |                 BENCHMARKS                |
            +              +---------------------+---------------------+
            |              | Current             | Census2020          |
            +==============+=====================+=====================+
            | **VINTAGES** | Current             | Census2020          |
            +              +---------------------+---------------------+
            |              | Census2020          | Census2010          |
            +              +---------------------+---------------------+
            |              | ACS2019             |                     |
            +              +---------------------+---------------------+
            |              | ACS2018             |                     |
            +              +---------------------+---------------------+
            |              | ACS2017             |                     |
            +              +---------------------+---------------------+
            |              | Census2010          |                     |
            +--------------+---------------------+---------------------+

        :type vintage: :class:`str <python:str>`

        :param layers: The set of geographic layers to return for the request. The default
          value is determined by the ``CENSUS_GEOCODER_LAYERS`` environment variable, and
          if that is not set defaults to ``'all'``.

            .. seealso::

              * :doc:`Geographies <geographies>` :ref:`Benchmarks, Vintages, and Layers <benchmarks_vintages_and_layers>`

        :type layers: :class:`str <python:str>`

        .. note::

          If more than one address-related parameter are supplied, this method will assume
          that a :term:`parametrized address` is provided.

        :returns: A given geographic entity.
        :rtype: :class:`GeographicEntity`

        :raises NoAddressError: if no address information is supplied
        :raises EntityNotFoundError: if no geographic entity was found matching the address
          supplied
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        if not args and not kwargs:
            raise errors.NoAddressError('No address information supplied.')

        if args:
            one_line = args[0]
        else:
            one_line = kwargs.get('one_line', None)

        street_1 = kwargs.get('street_1', None)
        city = kwargs.get('city', None)
        state = kwargs.get('state', None)
        zip_code = kwargs.get('zip_code', None)

        benchmark = kwargs.get('benchmark', DEFAULT_BENCHMARK)
        vintage = kwargs.get('vintage', DEFAULT_VINTAGE)

        layers = kwargs.get('layers', DEFAULT_LAYERS)

        if one_line:
            result = cls._get_one_line(one_line,
                                       benchmark = benchmark,
                                       vintage = vintage,
                                       layers = layers)
        else:
            result = cls._get_address(street_1 = street_1,
                                      city = city,
                                      state = state,
                                      zip_code = zip_code,
                                      benchmark = benchmark,
                                      vintage = vintage,
                                      layers = layers)

        return cls.from_json(result)

    @classmethod
    def from_batch(cls,
                   *args,
                   **kwargs):
        """Return geographic entities for a batch collection of inputs.

        :param file_: The name of a file in CSV, XLS/X, DAT, or TXT format. Expects the
          file to have the following columns *without a header row*:

          * Unique ID
          * Street Address
          * City
          * State
          * Zip Code

        :type file_: :class:`str <python:str>`

        :param benchmark: The name of the :term:`benchmark` of data to return. The default
          value is determined by the ``CENSUS_GEOCODER_BENCHMARK`` environment variable,
          and if that is not set defaults to ``'Current'`` which represents the current
          default benchmark, per the `Census Geocoder API`_.

          Accepts the following values:

            * ``'Current'`` (default)
            * ``'Census2020'``

        :type benchmark: :class:`str <python:str>`

        :param vintage: The vintage of Census data for which data should be returned. The
          default value is determined by the ``CENSUS_GEOCODER_VINTAGE`` environment
          variable, and if that is not set defaults to ``'Current'`` which represents the
          default vintage per the `Census Geocoder API`_.

          Acceptable values are dependent on the ``benchmark`` specified, as per the table below:

            +--------------+---------------------+---------------------+
            |              |                 BENCHMARKS                |
            +              +---------------------+---------------------+
            |              | Current             | Census2020          |
            +==============+=====================+=====================+
            | **VINTAGES** | Current             | Census2020          |
            +              +---------------------+---------------------+
            |              | Census2020          | Census2010          |
            +              +---------------------+---------------------+
            |              | ACS2019             |                     |
            +              +---------------------+---------------------+
            |              | ACS2018             |                     |
            +              +---------------------+---------------------+
            |              | ACS2017             |                     |
            +              +---------------------+---------------------+
            |              | Census2010          |                     |
            +--------------+---------------------+---------------------+

        :type vintage: :class:`str <python:str>`

        :param layers: The set of geographic layers to return for the request. The default
          value is determined by the ``CENSUS_GEOCODER_LAYERS`` environment variable, and
          if that is not set defaults to ``'all'``.

            .. seealso::

              * :doc:`Geographies <geographies>` :ref:`Benchmarks, Vintages, and Layers <benchmarks_vintages_and_layers>`

        :type layers: :class:`str <python:str>`

        :returns: A collection of geographic entities.
        :rtype: :class:`list <python:list>` of :class:`GeographicEntity`

        :raises NoFileProvidedError: if no ``file_`` is provided
        :raises FileNotFoundError: if ``file_`` does not exist on the filesystem
        :raises BatchSizeTooLargeError: if ``file_`` contains more than 10,000 records
        :raises EntityNotFoundError: if no geographic entity was found matching the
          address supplied
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        if args:
            file_ = args[0]
        else:
            file_ = kwargs.get('file_', None)

        if not file_:
            raise errors.NoFileProvidedError()

        file_ = validators.file_exists(file_, allow_empty = False)

        benchmark = kwargs.get('benchmark', DEFAULT_BENCHMARK)
        vintage = kwargs.get('vintage', DEFAULT_VINTAGE)

        layers = kwargs.get('layers', DEFAULT_LAYERS)

        result = cls._get_batch_addresses(file_ = file_,
                                          benchmark = benchmark,
                                          vintage = vintage,
                                          layers = layers)

        return [cls.from_csv_record(x) for x in result]

    @classmethod
    def from_coordinates(cls,
                         *args,
                         **kwargs):
        """Return data from a pair of geographic coordinates (longitude and latitude).

        :param longitude: The longitude coordinate.
        :type longitude: numeric

        :param latitude: The latitude coordinate.
        :type latitude: numeric

        :param benchmark: The name of the :term:`benchmark` of data to return. The default
          value is determined by the ``CENSUS_GEOCODER_BENCHMARK`` environment variable,
          and if that is not set defaults to ``'Current'`` which represents the current
          default benchmark, per the `Census Geocoder API`_.

          Accepts the following values:

            * ``'Current'`` (default)
            * ``'Census2020'``

        :type benchmark: :class:`str <python:str>`

        :param vintage: The vintage of Census data for which data should be returned. The
          default value is determined by the ``CENSUS_GEOCODER_VINTAGE`` environment
          variable, and if that is not set defaults to ``'Current'`` which represents the
          default vintage per the `Census Geocoder API`_.

          Acceptable values are dependent on the ``benchmark`` specified, as per the table below:

            +--------------+---------------------+---------------------+
            |              |                 BENCHMARKS                |
            +              +---------------------+---------------------+
            |              | Current             | Census2020          |
            +==============+=====================+=====================+
            | **VINTAGES** | Current             | Census2020          |
            +              +---------------------+---------------------+
            |              | Census2020          | Census2010          |
            +              +---------------------+---------------------+
            |              | ACS2019             |                     |
            +              +---------------------+---------------------+
            |              | ACS2018             |                     |
            +              +---------------------+---------------------+
            |              | ACS2017             |                     |
            +              +---------------------+---------------------+
            |              | Census2010          |                     |
            +--------------+---------------------+---------------------+

        :type vintage: :class:`str <python:str>`

        :param layers: The set of geographic layers to return for the request. The default
          value is determined by the ``CENSUS_GEOCODER_LAYERS`` environment variable, and
          if that is not set defaults to ``'all'``.

            .. seealso::

              * :doc:`Geographies <geographies>` :ref:`Benchmarks, Vintages, and Layers <benchmarks_vintages_and_layers>`

        :type layers: :class:`str <python:str>`

        .. note::

          If more than one address-related parameter are supplied, this method will assume
          that a :term:`parametrized address` is provided.

        :returns: A given geographic entity.
        :rtype: :class:`GeographicEntity`

        :raises NoAddressError: if no address information is supplied
        :raises EntityNotFound: if no geographic entity was found matching the address
          supplied
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        if not args and not kwargs:
            raise errors.NoAddressError('No coordinates supplied.')

        try:
            longitude = args[0]
        except (IndexError, TypeError):
            longitude = kwargs.get('longitude', None)
        try:
            latitude = args[1]
        except (IndexError, TypeError):
            latitude = kwargs.get('latitude', None)

        if not longitude and not latitude:
            raise errors.NoAddressError('No coordinates supplied.')
        elif not longitude:
            raise errors.NoAddressError('No longitude supplied.')
        elif not latitude:
            raise errors.NoAddressError('No latitude supplied.')

        longitude = validators.decimal(longitude, allow_empty = False)
        latitude = validators.decimal(latitude, allow_empty = False)

        benchmark = kwargs.get('benchmark', DEFAULT_BENCHMARK)
        vintage = kwargs.get('vintage', DEFAULT_VINTAGE)

        layers = kwargs.get('layers', DEFAULT_LAYERS)

        result = cls._get_coordinates(longitude = longitude,
                                      latitude = latitude,
                                      benchmark = benchmark,
                                      vintage = vintage,
                                      layers = layers)

        return cls.from_json(result)

    def inspect(self, as_census_fields = False):
        """Produce a list of the entity's properties that have values.

        :param as_census_fields: If ``True``, return property names as they appear in
          Census databases or the output of the `Census Geocoder API`_. If ``False``,
          return properties as they are defined on the **Census Geocoder** objects.
          Defaults to ``False``.
        :type as_census_fields: :class:`bool <python:bool>`

        :rtype: :class:`list <python:list>` of :class:`str <python:str>`
        """
        raise NotImplementedError()
