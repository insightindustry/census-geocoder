"""
###################################
census_geocoder/metaclasses.py
###################################

Defines the metaclasses that are used throughout the library.

"""
from abc import ABC, abstractmethod
import csv
import json

import requests
from validator_collection import validators
from backoff_utils import backoff

from census_geocoder import errors

CENSUS_API_URL = 'https://geocoding.geo.census.gov'

BENCHMARKS = {
    'CURRENT': 'Public_AR_Current',
    'TAB2020': 'Public_AR_TAB2020',
    'CENSUS2020': 'Public_AR_Census2020'
}

VINTAGES = {
    'Public_AR_Current': {
        'CURRENT': 'Current_Current',
        'CENSUS2020': 'Census2020_Current',
        'ACS2019': 'ACS2019_Current',
        'ACS2018': 'ACS2018_Current',
        'ACS2017': 'ACS2017_Current',
        'CENSUS2010': 'Census2010_Current'
    },
    'Public_AR_Census2020': {
        'CENSUS2020': 'Census2020_Census2020',
        'CENSUS2010': 'Census2010_Census2020'
    },
    'Public_AR_TAB2020': {
        'CURRENT': 'Current_TAB2020',
        'CENSUS2020': 'Census2020_TAB2020',
        'ACS2019': 'ACS2019_TAB2020',
        'ACS2018': 'ACS2018_TAB2020',
        'ACS2017': 'ACS2017_TAB2020',
        'CENSUS2010': 'Census2010_TAB2020'
    }
}


def parse_benchmark_vintage(benchmark = 'CURRENT', vintage = 'CURRENT'):
    """Parse the benchmark and vintage received.

    :param benchmark: The :term:`Benchmark` value to parse into its canonical form.
      Defaults to ``CURRENT``.
    :type benchmark: :class:`str <python:str>`

    :param vintage: The :term:`Vintage` value to parse into its canonical form.
      Defaults to ``CURRENT``.
    :type vintage: :class:`str <python:str>`

    :returns: The canonical ``(benchmark, vintage)``.
    :rtype: :class:`tuple <python:tuple>` of :class:`str <python:str>` and
      :class:`str <python:str>`

    :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
      recognized
    :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized within
      the ``benchmark`` specified

    """
    benchmark = validators.string(benchmark, allow_empty = False).upper()
    benchmark = BENCHMARKS.get(benchmark, None)
    if not benchmark:
        raise errors.UnrecognizedBenchmarkError(
            f'Benchmark ({benchmark}) is not a recognized benchmark.'
        )

    possible_vintages = VINTAGES.get(benchmark, None)
    vintage = validators.string(vintage, allow_empty = False).upper()
    vintage = possible_vintages.get(vintage, None)
    if not vintage:
        raise errors.UnrecognizedVintageError(
            f'Vintage ({vintage}) is not a recognized/available vintage within the '
            f'"{benchmark}" benchmark.'
        )

    return benchmark, vintage


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
        as_json = validators.json(as_json, allow_empty = False)

        return cls.from_dict(as_json)

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
                      benchmark = 'CURRENT',
                      vintage = 'CURRENT'):
        """Return data from a single-line address.

        :param one_line: The one-line address to geocode.
        :type one_line: :class:`str <python:str>`

        :param benchmark: The name of the :term:`benchmark` of data to return. Defaults to
          ``'Current'`` which represents the current default benchmark, per the Census
          Geocoder API. Accepts the following values:

          * ``'Current'`` (default)
          * ``'TAB2020'``
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

        :rtype: :class:`dict <python:dict>`

        :raises CensusAPIError: if the Census Geocoder API returned an error
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        one_line = validators.string(one_line)
        benchmark, vintage = parse_benchmark_vintage(benchmark, vintage)

        parameters = {
            'address': one_line,
            'benchmark': benchmark,
            'vintage': vintage,
            'format': 'json',
            'layers': 'all'
        }
        url = f'{CENSUS_API_URL}/geocoder/{cls.entity_type}/onelineaddress'

        result = backoff(requests.get,
                         args = [url],
                         kwargs = {'params': parameters},
                         max_tries = 5,
                         max_delay = 10)

        if result.status_code >= 400:
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
                     benchmark = 'CURRENT',
                     vintage = 'CURRENT'):
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

        :param benchmark: The name of the :term:`benchmark` of data to return. Defaults to
          ``'Current'`` which represents the current default benchmark, per the Census
          Geocoder API. Accepts the following values:

          * ``'Current'`` (default)
          * ``'TAB2020'``
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

        benchmark, vintage = parse_benchmark_vintage(benchmark, vintage)

        parameters = {
            'benchmark': benchmark,
            'vintage': vintage,
            'format': 'json',
            'layers': 'all'
        }
        is_valid = False
        if street_1:
            is_valid = True
            parameters['street_1'] = street_1
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

        url = f'{CENSUS_API_URL}/geocoder/{cls.entity_type}/address'

        result = backoff(requests.get,
                         args = [url],
                         kwargs = {'params': parameters},
                         max_tries = 5,
                         max_delay = 10)

        if result.status_code >= 400:
            raise errors.CensusAPIError(
                f'Census Geocoder API returned status code {result.status_code} with '
                f'message: "{result.text}".'
            )

        return result.json()

    @classmethod
    def _get_batch_addresses(cls,
                             file_,
                             benchmark = 'CURRENT',
                             vintage = 'CURRENT'):
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
          * ``'TAB2020'``
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

        :rtype: :class:`list <python:list>` of :class:`GeographicEntity`

        :raises NoFileProvidedError: if no ``file_`` is provided
        :raises FileNotFoundError: if ``file_`` does not exist on the filesystem
        :raises BatchSizeTooLargeError: if ``file_`` contains more than 10,000 records

        :raises CensusAPIError: if the Census Geocoder API returned an error
        :raises UnrecognizedBenchmarkError: if the ``benchmark`` supplied is not
          recognized
        :raises UnrecognizedVintageError: if the ``vintage`` supplied is not recognized

        """
        benchmark, vintage = parse_benchmark_vintage(benchmark, vintage)

        file_ = validators.file_exists(file_, allow_empty = False)
        file_length = check_length(file_)
        if file_length > 10000:
            raise errors.BatchSizeTooLargeError(f'Batch Too Large. Max of 10,000 entries '
                                                f'supported. File contains {file_length}')

        with open(file_, 'rb') as file_object:
            files = {
                'addressFile': (file_, file_object)
            }

        parameters = {
            'benchmark': benchmark,
            'vintage': vintage,
            'format': 'json',
            'layers': 'all'
        }

        url = f'{CENSUS_API_URL}/geocoder/{cls.entity_type}/addressbatch'

        result = backoff(requests.post,
                         args = [url],
                         kwargs = {
                             'files': files,
                             'params': parameters
                         },
                         max_tries = 5,
                         max_delay = 10)

        if result.status_code >= 400:
            raise errors.CensusAPIError(
                f'Census Geocoder API returned status code {result.status_code} with '
                f'message: "{result.text}".'
            )

        content = result.content.decode('utf-8')

        csv_reader = csv.reader(content.splitlines(), delimiter = ',')
        csv_list = list(csv_reader)

        return csv_list

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

        :param benchmark: The name of the :term:`benchmark` of data to return. Defaults to
          ``'Current'`` which represents the current default benchmark, per the Census
          Geocoder API. Accepts the following values:

          * ``'Current'`` (default)
          * ``'TAB2020'``
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

        .. note::

          If more than one parameter are supplied, this method will assume that a
          parametrized address is provided.

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
            raise errors.NoAddressError('No address information supplied.')

        if args:
            one_line = args[0]
        else:
            one_line = kwargs.get('one_line', None)

        street_1 = kwargs.get('street_1', None)
        city = kwargs.get('city', None)
        state = kwargs.get('state', None)
        zip_code = kwargs.get('zip_code', None)

        benchmark = kwargs.get('benchmark', 'CURRENT')
        vintage = kwargs.get('vintage', 'CURRENT')

        if one_line:
            result = cls._get_one_line(one_line,
                                       benchmark = benchmark,
                                       vintage = vintage)
        else:
            result = cls._get_address(street_1 = street_1,
                                      city = city,
                                      state = state,
                                      zip_code = zip_code,
                                      benchmark = benchmark,
                                      vintage = vintage)

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

        benchmark = kwargs.get('benchmark', 'CURRENT')
        vintage = kwargs.get('vintage', 'CURRENT')

        result = cls._from_batch_file(file_, benchmark, vintage)

        return [cls.from_list_item[x] for x in result]