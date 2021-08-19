"""
###################################
census_geocoder/locations.py
###################################

Defines :class:`Location` and :class:`MatchedAddress` geographic entities.

"""
from validator_collection import validators, checkers

from census_geocoder import errors, metaclasses, geographies


class MatchedAddress(metaclasses.BaseEntity):
    """Represents a matched address returned by the US Census GeoCoder API."""

    def __init__(self, **kwargs):
        self._tigerline_side = None
        self._tigerline_id = None

        self._latitude = None
        self._longitude = None

        self._address = None

        self._from_address = None
        self._to_address = None
        self._street = None
        self._pre_type = None
        self._pre_direction = None
        self._pre_qualifier = None
        self._suffix_type = None
        self._suffix_direction = None
        self._suffix_qualifier = None
        self._city = None
        self._state = None
        self._zip_code = None

        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs.get(key, None))

    @property
    def tigerline_id(self):
        """The TigerLine ID for the matched address.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._tigerline_id

    @tigerline_id.setter
    def tigerline_id(self, value):
        self._tigerline_id = validators.string(value, allow_empty = True)

    @property
    def tigerline_side(self):
        """The TigerLine side of the street for the matched address. Accepts either 'L' or
        'R'.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._tigerline_side

    @tigerline_side.setter
    def tigerline_side(self, value):
        value = validators.string(value, allow_empty = True)
        if value:
            value = value.upper()
        if value and value not in ['L', 'R']:
            raise ValueError(
                f'tigerline_side can only be None, "L", or "R". Was: {value}'
            )
        self._tigerline_side = value

    @property
    def longitude(self):
        """The longitude coordinate for the location.

        :rtype: :class:`decimal <python:decimal.decimal>`
        """
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = validators.decimal(value, allow_empty = True)

    @property
    def latitude(self):
        """The latitude coordinate for the location.

        :rtype: :class:`decimal <python:decimal.decimal>`
        """
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = validators.decimal(value, allow_empty = True)

    @property
    def address(self):
        """The canonical address that was matched for the :class:`Location`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._address

    @address.setter
    def address(self, value):
        self._address = validators.string(value, allow_empty = True)

    @property
    def pre_type(self):
        """The canonical pre-type that was matched for the :class:`Location`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._pre_type

    @pre_type.setter
    def pre_type(self, value):
        self._pre_type = validators.string(value, allow_empty = True)

    @property
    def suffix_type(self):
        """The canonical suffix-type that was matched for the :class:`Location`.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._suffix_type

    @suffix_type.setter
    def suffix_type(self, value):
        self._suffix_type = validators.string(value, allow_empty = True)

    @property
    def pre_qualifier(self):
        """The canonical pre-qualifier that was matched for the :class:`Location`.

        :rqualifier: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._pre_qualifier

    @pre_qualifier.setter
    def pre_qualifier(self, value):
        self._pre_qualifier = validators.string(value, allow_empty = True)

    @property
    def suffix_qualifier(self):
        """The canonical suffix-qualifier that was matched for the :class:`Location`.

        :rqualifier: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._suffix_qualifier

    @suffix_qualifier.setter
    def suffix_qualifier(self, value):
        self._suffix_qualifier = validators.string(value, allow_empty = True)

    @property
    def pre_direction(self):
        """The canonical pre-direction that was matched for the :class:`Location`.

        :rdirection: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._pre_direction

    @pre_direction.setter
    def pre_direction(self, value):
        self._pre_direction = validators.string(value, allow_empty = True)

    @property
    def suffix_direction(self):
        """The canonical suffix-direction that was matched for the :class:`Location`.

        :rdirection: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._suffix_direction

    @suffix_direction.setter
    def suffix_direction(self, value):
        self._suffix_direction = validators.string(value, allow_empty = True)

    @property
    def from_address(self):
        """The canonical lower-bound street number that was matched for the
        :class:`Location`.

        :rdirection: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._from_address

    @from_address.setter
    def from_address(self, value):
        self._from_address = validators.string(value, allow_empty = True)

    @property
    def to_address(self):
        """The canonical upper-bound street number that was matched for the
        :class:`Location`.

        :rdirection: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._to_address

    @to_address.setter
    def to_address(self, value):
        self._to_address = validators.string(value, allow_empty = True)

    @property
    def street(self):
        """The canonical street name that was matched for the :class:`Location`.

        :rdirection: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._street

    @street.setter
    def street(self, value):
        self._street = validators.string(value, allow_empty = True)

    @property
    def city(self):
        """The canonical city name that was matched for the :class:`Location`.

        :rdirection: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._city

    @city.setter
    def city(self, value):
        self._city = validators.string(value, allow_empty = True)

    @property
    def state(self):
        """The canonical state that was matched for the :class:`Location`.

        :rdirection: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._state

    @state.setter
    def state(self, value):
        self._state = validators.string(value, allow_empty = True)

    @property
    def zip_code(self):
        """The canonical zip code that was matched for the :class:`Location`.

        :rdirection: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._zip_code

    @zip_code.setter
    def zip_code(self, value):
        self._zip_code = validators.string(value, allow_empty = True)

    @property
    def entity_type(self):
        return 'address'

    @classmethod
    def from_csv_record(cls, csv_record):
        """Create an instance of the geographic entity from its CSV record.

        :param csv_record: The list of columns for the CSV record.
        :type csv_record: :class:`list <python:list>` of :class:`str <python:str>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`GeographicEntity`

        """
        csv_record = validators.iterable(csv_record, allow_empty = False)

        one_line_address = csv_record[1]
        matched_address = csv_record[4]

        coordinates = csv_record[5].split(',')
        longitude = coordinates[0]
        latitude = coordinates[1]

        tigerline_id = csv_record[6]
        tigerline_side = csv_record[7]

        state_fips_code = csv_record[8]
        county_fips_code = csv_record[9]
        census_tract_fips = csv_record[10]
        census_block_fips = csv_record[11]

        return cls(address = matched_address,
                   longitude = longitude,
                   latitude = latitude,
                   tigerline_id = tigerline_id,
                   tigerline_side = tigerline_side)

    def from_dict(cls, as_dict):
        """Create an instance of the geographic entity from its
        :class:`dict <python:dict>` representation.

        :param as_dict: The :class:`dict <python:dict>` representation of the geographic
          entity.
        :type as_dict: :class:`dict <python:dict>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`GeographicEntity`

        """
        as_dict = validators.dict(as_dict, allow_empty = False)

        address = as_dict.get('result', {})\
                                 .get('addressMatches', {})\
                                 .get('address', None)

        longitude = as_dict.get('result', {})\
                           .get('addressMatches', {})\
                           .get('coordinates', {})\
                           .get('x', None)
        latitude = as_dict.get('result', {})\
                          .get('addressMatches', {})\
                          .get('coordinates', {})\
                          .get('y', None)

        tigerline_side = as_dict.get('result', {})\
                                .get('addressMatches', {})\
                                .get('tigerLine', {})\
                                .get('side', None)
        tigerline_id = as_dict.get('result', {})\
                              .get('addressMatches', {})\
                              .get('tigerLine', {})\
                              .get('tigerLineId', None)

        pre_type = as_dict.get('result', {})\
                          .get('addressMatches', {})\
                          .get('addressComponents', {})\
                          .get('preType', None)
        suffix_type = as_dict.get('result', {})\
                             .get('addressMatches', {})\
                             .get('addressComponents', {})\
                             .get('suffixType', None)
        pre_qualifier = as_dict.get('result', {})\
                               .get('addressMatches', {})\
                               .get('addressComponents', {})\
                               .get('preQualifier', None)
        suffix_qualifier = as_dict.get('result', {})\
                                  .get('addressMatches', {})\
                                  .get('addressComponents', {})\
                                  .get('suffixQualifier', None)
        pre_direction = as_dict.get('result', {})\
                               .get('addressMatches', {})\
                               .get('addressComponents', {})\
                               .get('preDirection', None)
        suffix_direction = as_dict.get('result', {})\
                                  .get('addressMatches', {})\
                                  .get('addressComponents', {})\
                                  .get('suffixDirection', None)
        from_address = as_dict.get('result', {})\
                              .get('addressMatches', {})\
                              .get('addressComponents', {})\
                              .get('fromAddress', None)
        to_address = as_dict.get('result', {})\
                            .get('addressMatches', {})\
                            .get('addressComponents', {})\
                            .get('toAddress', None)
        street = as_dict.get('result', {})\
                        .get('addressMatches', {})\
                        .get('addressComponents', {})\
                        .get('streetName', None)
        city = as_dict.get('result', {})\
                      .get('addressMatches', {})\
                      .get('addressComponents', {})\
                      .get('city', None)
        state = as_dict.get('result', {})\
                       .get('addressMatches', {})\
                       .get('addressComponents', {})\
                       .get('state', None)
        zip_code = as_dict.get('result', {})\
                          .get('addressMatches', {})\
                          .get('addressComponents', {})\
                          .get('zip', None)

        return cls({
            'tigerline_id': tigerline_id,
            'tigerline_side': tigerline_side,
            'longitude': longitude,
            'latitute': latitude,
            'pre_type': pre_type,
            'suffix_type': suffix_type,
            'pre_qualifier': pre_qualifier,
            'suffix_qualifier': suffix_qualifier,
            'pre_direction': pre_direction,
            'suffix_direction': suffix_direction,
            'from_address': from_address,
            'to_address': to_address,
            'street': street,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'address': address
        })

    def to_dict(self):
        """Returns a :class:`dict <python:dict>` representation of the geographic entity.

        .. note::

          The :class:`dict <python:dict>` representation matches the JSON structure for
          the US Census Geocoder API. This is a not-very-pythonic
          :class:`dict <python:dict>` structure, but at least this ensures idempotency.

        :returns: :class:`dict <python:dict>` representation of the entity.
        :rtype: :class:`dict <python:dict>`

        """
        result = {
            'matchedAddress': self.address,
            'coordinates': {
                'x': self.longitude,
                'y': self.latitude
            },
            'tigerLine': {
                'tigerLineId': self.tigerline_id,
                'side': self.tigerline_side
            },
            'addressComponents': {
                'fromAddress': self.from_address,
                'toAddress': self.to_address,
                'preType': self.pre_type,
                'preQualifier': self.pre_qualifier,
                'preDirection': self.pre_direction,
                'streetName': self.street,
                'suffixType': self.suffix_type,
                'suffixQualifier': self.suffix_qualifier,
                'suffixDirection': self.suffix_direction,
                'city': self.city,
                'state': self.state,
                'zip': self.zip_code
            },
            'geographies': [x.to_dict() for x in self.geographies]
        }

        return result


class Location(metaclasses.GeographicEntity):
    """Represents a specific location returned by the US Census Geocoder API."""

    def __init__(self, **kwargs):
        self._input_one_line = None
        self._input_street = None
        self._input_city = None
        self._input_state = None
        self._input_zip_code = None

        self._benchmark_name = None
        self._benchmark_description = None
        self._benchmark_id = None
        self._benchmark_is_default = False

        self._vintage_name = None
        self._vintage_description = None
        self._vintage_id = None
        self._vintage_is_default = False

        self._matched_addresses = None

        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs.get(key, None))

    @property
    def input_one_line(self):
        """The one-line address that was provided as input to get this :class:`Location`.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._input_one_line

    @input_one_line.setter
    def input_one_line(self, value):
        self._input_one_line = validators.string(value, allow_empty = True)

    @property
    def input_street(self):
        """The street address that was provided as input to get this :class:`Location`.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._input_street

    @input_street.setter
    def input_street_1(self, value):
        self._input_street = validators.string(value, allow_empty = True)

    @property
    def input_city(self):
        """The city that was provided as input to get this :class:`Location`.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._input_city

    @input_city.setter
    def input_city(self, value):
        self._input_city = validators.string(value, allow_empty = True)

    @property
    def input_state(self):
        """The state that was provided as input to get this :class:`Location`.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._input_state

    @input_state.setter
    def input_state(self, value):
        self._input_state = validators.string(value, allow_empty = True)

    @property
    def input_zip_code(self):
        """The zip code that was provided as input to get this :class:`Location`.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._input_zip_code

    @input_zip_code.setter
    def input_zip_code(self, value):
        self._input_zip_code = validators.string(value, allow_empty = True)

    @property
    def input_address(self):
        """Returns a :class:`dict <python:dict>` with the input address provided.

        :rtype: :class:`dict <python:dict>`
        """
        result = {}
        if self.input_one_line:
            result['address'] = self.input_one_line

        if self.input_street:
            result['street'] = self.input_street

        if self.input_city:
            result['city'] = self.input_city

        if self.input_state:
            result['state'] = self.input_state

        if self.input_zip_code:
            result['zip_code'] = self.zip_code

        return result

    @property
    def benchmark_name(self):
        """The name of the :term:`benchmark` for which this data was returned.

        :rtype: :class:`str <python:str>`
        """
        return self._benchmark_name

    @benchmark_name.setter
    def benchmark_name(self, value):
        self._benchmark_name = validators.string(value, allow_empty = True)

    @property
    def benchmark_description(self):
        """The description of the :term:`benchmark` for which this data was returned.

        :rtype: :class:`str <python:str>`
        """
        return self._benchmark_description

    @benchmark_description.setter
    def benchmark_description(self, value):
        self._benchmark_description = validators.string(value, allow_empty = True)

    @property
    def benchmark_id(self):
        """The name of the :term:`benchmark` for which this data was returned.

        :rtype: :class:`str <python:str>`
        """
        return self._benchmark_id

    @benchmark_id.setter
    def benchmark_id(self, value):
        self._benchmark_id = validators.string(value, allow_empty = True)

    @property
    def benchmark_is_default(self):
        """If ``True``, indicates that the default :term:`benchmark` has been applied.

        :rtype: :class:`bool <python:bool>`
        """
        return bool(self._benchmark_is_default)

    @benchmark_is_default.setter
    def benchmark_is_default(self, value):
        self._benchmark_is_default = bool(value)

    @property
    def benchmark(self):
        """The short-hand value of the benchmark for which this :class:`Location` was
        calculated.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        for key in metaclasses.BENCHMARKS:
            if metaclasses.BENCHMARKS.get(key, None) == self.benchmark_name:
                return key

        return None

    @property
    def vintage_name(self):
        """The name of the :term:`vintage` for which this data was returned.

        :rtype: :class:`str <python:str>`
        """
        return self._vintage_name

    @vintage_name.setter
    def vintage_name(self, value):
        self._vintage_name = validators.string(value, allow_empty = True)

    @property
    def vintage_description(self):
        """The description of the :term:`vintage` for which this data was returned.

        :rtype: :class:`str <python:str>`
        """
        return self._vintage_description

    @vintage_description.setter
    def vintage_description(self, value):
        self._vintage_description = validators.string(value, allow_empty = True)

    @property
    def vintage_id(self):
        """The name of the :term:`vintage` for which this data was returned.

        :rtype: :class:`str <python:str>`
        """
        return self._vintage_id

    @vintage_id.setter
    def vintage_id(self, value):
        self._vintage_id = validators.string(value, allow_empty = True)

    @property
    def vintage_is_default(self):
        """If ``True``, indicates that the default :term:`vintage` has been applied.

        :rtype: :class:`bool <python:bool>`
        """
        return bool(self._vintage_is_default)

    @vintage_is_default.setter
    def vintage_is_default(self, value):
        self._vintage_is_default = bool(value)

    @property
    def matched_addresses(self):
        """Collection of addresses that have been matched to the :class:`Location`.

        :rtype: :class:`list <python:list>` of :class:`MatchedAddress` /
          :obj:`None <python:None>`
        """
        return self._matched_addresses

    @matched_addresses.setter
    def matched_addresses(self, value):
        value = validators.iterable(value, allow_empty = True)
        for item in value:
            if checkers.is_type(item, 'MatchedAddress') is False:
                raise ValueError(
                    f'item must be a MatchedAddress. Was: {item.__class__.__name__}'
                )

        self._matched_addresses = [x for x in value]

    @property
    def entity_type(self):
        return 'locations'

    @classmethod
    def from_csv_record(cls, csv_record):
        """Create an instance of the geographic entity from its CSV record.

        :param csv_record: The list of columns for the CSV record.
        :type csv_record: :class:`list <python:list>` of :class:`str <python:str>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`GeographicEntity`

        """
        csv_record = validators.iterable(csv_record, allow_empty = False)

        one_line_address = csv_record[1]
        matched_address = csv_record[4]

        coordinates = csv_record[5].split(',')
        longitude = coordinates[0]
        latitude = coordinates[1]

        tigerline_id = csv_record[6]
        tigerline_side = csv_record[7]

        state_fips_code = csv_record[8]
        county_fips_code = csv_record[9]
        census_tract_fips = csv_record[10]
        census_block_fips = csv_record[11]

        matched_address = MatchedAddress(address = matched_address,
                                         longitude = longitude,
                                         latitude = latitude,
                                         tigerline_id = tigerline_id,
                                         tigerline_side = tigerline_side)

        return cls(input_one_line = one_line_address,
                   matched_addresses = [matched_address])

    @classmethod
    def from_dict(cls, as_dict):
        """Create an instance of the geographic entity from its
        :class:`dict <python:dict>` representation.

        :param as_dict: The :class:`dict <python:dict>` representation of the geographic
          entity.
        :type as_dict: :class:`dict <python:dict>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`GeographicEntity`

        """
        as_dict = validators.dict(as_dict, allow_empty = False)

        input_one_line = as_dict.get('result', {})\
                                .get('input', {})\
                                .get('address', {})\
                                .get('address', None)
        input_street = as_dict.get('result', {})\
                              .get('input', {})\
                              .get('address', {})\
                              .get('street', None)
        input_city = as_dict.get('result', {})\
                            .get('input', {})\
                            .get('address', {})\
                            .get('city', None)
        input_state = as_dict.get('result', {})\
                             .get('input', {})\
                             .get('address', {})\
                             .get('state', None)
        input_zip_code = as_dict.get('result', {})\
                                .get('input', {})\
                                .get('address', {})\
                                .get('zip', None)

        benchmark_name = as_dict.get('result', {})\
                                .get('input', {})\
                                .get('benchmark', {})\
                                .get('benchmarkName', None)
        benchmark_id = as_dict.get('result', {})\
                              .get('input', {})\
                              .get('benchmark', {})\
                              .get('id', None)
        benchmark_description = as_dict.get('result', {})\
                                       .get('input', {})\
                                       .get('benchmark', {})\
                                       .get('benchmarkDescription', None)
        benchmark_is_default = as_dict.get('result', {})\
                                      .get('input', {})\
                                      .get('benchmark', {})\
                                      .get('isDefault', False)

        vintage_name = as_dict.get('result', {})\
                                .get('input', {})\
                                .get('vintage', {})\
                                .get('vintageName', None)
        vintage_id = as_dict.get('result', {})\
                              .get('input', {})\
                              .get('vintage', {})\
                              .get('id', None)
        vintage_description = as_dict.get('result', {})\
                                       .get('input', {})\
                                       .get('vintage', {})\
                                       .get('vintageDescription', None)
        vintage_is_default = as_dict.get('result', {})\
                                      .get('input', {})\
                                      .get('vintage', {})\
                                      .get('isDefault', False)

        matched_addresses = as_dict.get('result', {})\
                                   .get('addressMatches', [])

        matched_addresses = [MatchedAddress.from_json(x) for x in matched_addresses]

        return cls({
            'input_one_line': input_one_line,
            'input_street': input_street,
            'input_city': input_city,
            'input_state': input_state,
            'input_zip_code': input_zip_code,
            'benchmark_name': benchmark_name,
            'benchmark_description': benchmark_description,
            'benchmark_is_default': benchmark_is_default,
            'benchmark_id': benchmark_id,
            'vintage_name': vintage_name,
            'vintage_description': vintage_description,
            'vintage_is_default': vintage_is_default,
            'vintage_id': vintage_id,
            'matched_addresses': matched_addresses
        })

    def to_dict(self):
        """Returns a :class:`dict <python:dict>` representation of the geographic entity.

        .. note::

          The :class:`dict <python:dict>` representation matches the JSON structure for
          the US Census Geocoder API. This is a not-very-pythonic
          :class:`dict <python:dict>` structure, but at least this ensures idempotency.

        :returns: :class:`dict <python:dict>` representation of the entity.
        :rtype: :class:`dict <python:dict>`

        """
        result = {
            'input': {
                'address': {},
                'benchmark': {
                    'id': self.benchmark_id,
                    'benchmarkName': self.benchmark_name,
                    'benchmarkDescription': self.benchmark_description,
                    'isDefault': self.benchmark_is_default
                },
                'vintage': {
                    'id': self.vintage_id,
                    'vintageName': self.vintage_name,
                    'vintageDescription': self.vintage_description,
                    'isDefault': self.vintage_is_default
                }
            }
        }

        if self.input_one_line:
            result['input']['address']['address'] = self.input_one_line
        if self.input_street:
            result['input']['address']['street'] = self.input_street
        if self.input_city:
            result['input']['address']['city'] = self.input_city
        if self.input_state:
            result['input']['address']['state'] = self.input_state
        if self.input_zip_code:
            result['input']['address']['zip'] = self.input_zip_code
