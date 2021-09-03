"""
###################################
census_geocoder/geographies.py
###################################

Defines :class:`Geography` geographic entities.

"""
from inspect import currentframe

from validator_collection import validators, checkers

from census_geocoder import metaclasses, errors
from census_geocoder.constants import FUNCSTAT, LSAD


class GeographicArea(metaclasses.GeographicEntity):
    """Base class for a given :term:`geography` as supported by the US government."""

    def __init__(self, **kwargs):
        self._geoid = None
        self._oid = None
        self._object_id = None
        self._name = None
        self._basename = None
        self._funcstat = None
        self._lsad = None

        self._legislative_session_year = None

        self._state_fips_code = None
        self._state_ns = None
        self._state_abbreviation = None

        self._division_fips_code = None
        self._region_fips_code = None

        self._tract = None
        self._block = None
        self._block_group = None
        self._lwblk_typ = None

        self._county_fips_code = None
        self._county_cc = None
        self._county_ns = None
        self._cousub_cc = None
        self._cousub_ns = None

        self._place = None
        self._place_cc = None
        self._place_ns = None

        self._necta_pci = None
        self._cbsa_pci = None

        self._congressional_session_code = None

        self._zcta5 = None
        self._zcta5_cc = None

        self._school_district_type = None
        self._sduni = None
        self._low_school_grade = None
        self._high_school_grade = None

        self._vtd = None
        self._vtdi = None

        self._metdiv = None
        self._csa = None
        self._cbsa = None

        self._latitude = None
        self._longitude = None
        self._latitude_internal_point = None
        self._longitude_internal_point = None

        self._water_area = None
        self._land_area = None

        self._pop100 = None
        self._hu100 = None
        self._sldu = None
        self._sldl = None
        self._mtfcc = None
        self._ldtyp = None

        self._ur = None
        self.extensions = {}

        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs.get(key, None))
            else:
                self.extensions[key] = kwargs.get(key, None)

    @property
    def geoid(self):
        """The Geographic Identifier.

        .. note::

          Fully concatenated geographic code (State FIPS and component numbers).

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._geoid

    @geoid.setter
    def geoid(self, value):
        self._geoid = validators.string(value, allow_empty = True)

    @property
    def oid(self):
        """The OID.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._oid

    @oid.setter
    def oid(self, value):
        self._oid = validators.string(value, allow_empty = True)

    @property
    def object_id(self):
        """The Object Identifier.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._object_id

    @object_id.setter
    def object_id(self, value):
        self._object_id = validators.numeric(value, allow_empty = True)

    @property
    def name(self):
        """The human-readable name of the geography.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = validators.string(value, allow_empty = True)

    @property
    def basename(self):
        """The human-readable basename of the geography.

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._basename

    @basename.setter
    def basename(self, value):
        self._basename = validators.string(value, allow_empty = True)

    @property
    def functional_status(self):
        """The functional status of the geography.

        .. seealso::

          * `Functional Status Codes and Definitions <https://www.census.gov/library/reference/code-lists/functional-status-codes.html>`_

        :rtype: :class:`str <python:str>`
        """
        return FUNCSTAT.get(self.funcstat, None)

    @property
    def funcstat(self):
        """The functional status code of the geography.

        .. seealso::

          * `Functional Status Codes and Definitions <https://www.census.gov/library/reference/code-lists/functional-status-codes.html>`_

        :rtype: :class:`str <python:str>`
        """
        return FUNCSTAT.get(self._funcstat, None)

    @funcstat.setter
    def funcstat(self, value):
        value = validators.string(value, allow_empty = True)
        if value and value.upper() not in FUNCSTAT:
            raise ValueError(f'value ("{value}") not a recognized FUNCSTAT code')

        if value:
            self._funcstat = value.upper()
        else:
            self._funcstat = None

    @property
    def lsad(self):
        """Legal/Statisical Area Descriptor (LSAD) Code

        .. seealso::

          * `Legal/Statistical Area Descriptor Codes and Definitions <https://www.census.gov/library/reference/code-lists/legal-status-codes.html>`_

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._lsad

    @lsad.setter
    def lsad(self, value):
        value = validators.string(value, allow_empty = True)
        if value and value.upper() in LSAD:
            value = value.upper()

        self._lsad = value

    @property
    def legal_statistical_area(self):
        """Legal/Statistical Area Descriptor

        .. seealso::

          * `Legal/Statistical Area Descriptor Codes and Definitions <https://www.census.gov/library/reference/code-lists/legal-status-codes.html>`_

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        if not self.lsad:
            return None
        result = LSAD.get(self.lsad, None)
        if result and '(suffix)' in result:
            result = result.replace(' (suffix)', '')
        if result and '(prefix)' in result:
            result = result.replace(' (prefix)', '')
        if result and '(balance)' in result:
            result = result.replace(' (balance)', '')

        return result

    @property
    def lsad_category(self):
        """Indicates the category of the LSAD for the geography. Returns either:

            * Unspecified
            * Prefix
            * Suffix
            * Balance

        :rtype: :class:`str <python:str>`
        """
        result = "Unspecified"
        lsad = LSAD.get(self.lsad, '')
        if '(prefix)' in lsad:
            result = 'Prefix'
        elif '(suffix)' in lsad:
            result = 'Suffix'
        elif '(balance)' in lsad:
            result = 'Balance'

        return result

    @property
    def legislative_session_year(self):
        """Legislative Session Year (``LSY``)

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._legislative_session_year

    @legislative_session_year.setter
    def legislative_session_year(self, value):
        value = validators.string(value, allow_empty = True)
        if value and not len(value) == 4:
            raise ValueError('legislative_session_year expects 4-digit year as a string')

        self._legislative_session_year = value

    @property
    def state_fips_code(self):
        """State FIPS Code

        :rtype: :class:`str <python:str>`
        """
        return self._state_fips_code

    @state_fips_code.setter
    def state_fips_code(self, value):
        self._state_fips_code = validators.string(value, allow_empty = True)

    @property
    def state_ns(self):
        """State ANSI Feature Code

        :rtype: :class:`str <python:str>`
        """
        return self._state_ns

    @state_ns.setter
    def state_ns(self, value):
        self._state_ns = validators.string(value, allow_empty = True)

    @property
    def state_abbreviation(self):
        """State Abbreviation

        :rtype: :class:`str <python:str>`
        """
        return self._state_abbreviation

    @state_abbreviation.setter
    def state_abbreviation(self, value):
        value = validators.string(value, allow_empty = True)
        if value:
            value = value.upper()

        self._state_abbreviation = value

    @property
    def division_fips_code(self):
        """State FIPS Code

        :rtype: :class:`str <python:str>`
        """
        return self._division_fips_code

    @division_fips_code.setter
    def division_fips_code(self, value):
        self._division_fips_code = validators.string(value, allow_empty = True)

    @property
    def region_fips_code(self):
        """Region FIPS Code

        :rtype: :class:`str <python:str>`
        """
        return self._region_fips_code

    @region_fips_code.setter
    def region_fips_code(self, value):
        self._region_fips_code = validators.string(value, allow_empty = True)

    @property
    def tract(self):
        """Census Tract Code

        :rtype: :class:`str <python:str>`
        """
        return self._tract

    @tract.setter
    def tract(self, value):
        self._tract = validators.string(value, allow_empty = True)

    @property
    def block(self):
        """Census Block Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._block

    @block.setter
    def block(self, value):
        self._block = validators.string(value, allow_empty = True)

    @property
    def block_group(self):
        """Census Block Group Code

        :rtype: :class:`str <python:str>`
        """
        return self._block_group

    @block_group.setter
    def block_group(self, value):
        self._block_group = validators.string(value, allow_empty = True)

    @property
    def county_fips_code(self):
        """County FIPS Code

        :rtype: :class:`str <python:str>`
        """
        return self._county_fips_code

    @county_fips_code.setter
    def county_fips_code(self, value):
        self._county_fips_code = validators.string(value, allow_empty = True)

    @property
    def county_cc(self):
        """County Class Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._county_cc

    @county_cc.setter
    def county_cc(self, value):
        self._county_cc = validators.string(value, allow_empty = True)

    @property
    def county_ns(self):
        """County ANSI Feature Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._county_ns

    @county_ns.setter
    def county_ns(self, value):
        self._county_ns = validators.string(value, allow_empty = True)

    @property
    def place(self):
        """Census Place Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._place

    @place.setter
    def place(self, value):
        self._place = validators.string(value, allow_empty = True)

    @property
    def place_cc(self):
        """Place Class Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._place_cc

    @place_cc.setter
    def place_cc(self, value):
        self._place_cc = validators.string(value, allow_empty = True)

    @property
    def place_ns(self):
        """Place ANSI Feature Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._place_ns

    @place_ns.setter
    def place_ns(self, value):
        self._place_ns = validators.string(value, allow_empty = True)

    @property
    def necta_pci(self):
        """NECTA Principal City Indciator

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._necta_pci

    @necta_pci.setter
    def necta_pci(self, value):
        value = validators.string(value, allow_empty = True)
        if value and len(value) > 1:
            raise ValueError(
                f'necta_pci expects a 1-character value. Received: {len(value)}'
            )
        if value:
            self._necta_pci = value.upper()
        else:
            self._necta_pci = value

    @property
    def cbsa_pci(self):
        """CBSA Principal City Indciator

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._cbsa_pci

    @cbsa_pci.setter
    def cbsa_pci(self, value):
        value = validators.string(value, allow_empty = True)
        if value and len(value) > 1:
            raise ValueError(
                f'cbsa_pci expects a 1-character value. Received: {len(value)}'
            )
        if value:
            self._cbsa_pci = value.upper()
        else:
            self._cbsa_pci = value

    @property
    def is_principal_city(self):
        """If ``True``, indicates that the geography is the principal city of its
        surrounding entity.

        :rtype: :class:`bool <python:bool>`
        """
        return self.cbsa_pci == 'Y' or self.necta_pci == 'Y'

    @property
    def congressional_session_code(self):
        """Congressional Session Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._congressional_session_code

    @congressional_session_code.setter
    def congressional_session_code(self, value):
        self._congressional_session_code = validators.string(value, allow_empty = True)

    @property
    def zcta5(self):
        """ZCTA-5 Zip Code Value

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._zcta5

    @zcta5.setter
    def zcta5(self, value):
        self._zcta5 = validators.string(value, allow_empty = True)

    @property
    def zcta5_cc(self):
        """ZCTA5 Class Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._zcta5_cc

    @zcta5_cc.setter
    def zcta5_cc(self, value):
        self._zcta5_cc = validators.string(value, allow_empty = True)

    @property
    def school_district_type(self):
        """School District Type

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._school_district_type

    @school_district_type.setter
    def school_district_type(self, value):
        self._school_district_type = validators.string(value, allow_empty = True)

    @property
    def low_school_grade(self):
        """School District - Lowest Grade

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._low_school_grade

    @low_school_grade.setter
    def low_school_grade(self, value):
        self._low_school_grade = validators.string(value, allow_empty = True)

    @property
    def high_school_grade(self):
        """School District - Highest Grade

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._high_school_grade

    @high_school_grade.setter
    def high_school_grade(self, value):
        self._high_school_grade = validators.string(value, allow_empty = True)

    @property
    def csa(self):
        """Census CSA Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._csa

    @csa.setter
    def csa(self, value):
        self._csa = validators.string(value, allow_empty = True)

    @property
    def cbsa(self):
        """Census CBSA Code

        :rtype: :class:`str <python:str>` / :obj:`None <python:None>`
        """
        return self._cbsa

    @cbsa.setter
    def cbsa(self, value):
        self._cbsa = validators.string(value, allow_empty = True)

    @property
    def latitude(self):
        """The :term:`centroid latitude` for the geographic area.

        :rtype: :class:`Decimal <python:decimal.Decimal>` / :obj:`None <python:None>`
        """
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        value = validators.string(value, allow_empty = True)
        if value and value.startswith('+'):
            value = value[1:]
        if value and value.startswith('0'):
            value = value[1:]

        self._latitude = validators.decimal(value, allow_empty = True)

    @property
    def latitude_internal_point(self):
        """The :term:`internal point latitude` for the geographic area.

        :rtype: :class:`Decimal <python:decimal.Decimal>` / :obj:`None <python:None>`
        """
        return self._latitude_internal_point

    @latitude_internal_point.setter
    def latitude_internal_point(self, value):
        value = validators.string(value, allow_empty = True)
        if value and value.startswith('+'):
            value = value[1:]
        if value and value.startswith('0'):
            value = value[1:]

        self._latitude_internal_point = validators.decimal(value, allow_empty = True)

    @property
    def longitude(self):
        """The :term:`centroid longitude` for the geographic area.

        :rtype: :class:`Decimal <python:decimal.Decimal>` / :obj:`None <python:None>`
        """
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        value = validators.string(value, allow_empty = True)
        if value and value.startswith('+'):
            value = value[1:]
        if value and value.startswith('0'):
            value = value[1:]

        self._longitude = validators.decimal(value, allow_empty = True)

    @property
    def longitude_internal_point(self):
        """The :term:`internal point longitude` for the geographic area.

        :rtype: :class:`Decimal <python:decimal.Decimal>` / :obj:`None <python:None>`
        """
        return self._longitude_internal_point

    @longitude_internal_point.setter
    def longitude_internal_point(self, value):
        value = validators.string(value, allow_empty = True)
        if value and value.startswith('+'):
            value = value[1:]
        if value and value.startswith('0'):
            value = value[1:]

        self._longitude_internal_point = validators.decimal(value, allow_empty = True)

    @property
    def water_area(self):
        """The area of the geography that is covered in water, expressed in square meters.

        .. note::

          Water area calculations in this table include only perennial water. All other
          water (intermittent, glacier, and marsh/swamp) is included in this table as part
          of :meth:`land_area <Geography.land_area>` calculations.

        :rtype: :class:`int <python:int>` / :obj:`None <python:None>`
        """
        return self._water_area

    @water_area.setter
    def water_area(self, value):
        self._water_area = validators.integer(value, allow_empty = True, minimum = 0)

    @property
    def land_area(self):
        """The area of the geography that is on solid land, expressed in square meters.

        :rtype: :class:`int <python:int>` / :obj:`None <python:None>`
        """
        return self._land_area

    @land_area.setter
    def land_area(self, value):
        self._land_area = validators.integer(value, allow_empty = True, minimum = 0)

    @property
    def entity_type(self):
        return 'geographies'

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        raise TypeError('Not supported at the base class level.')

    @classmethod
    def from_csv_record(cls, csv_record):
        """Create an instance of the geographic entity from its CSV record.

        :param csv_record: The list of columns for the CSV record.
        :type csv_record: :class:`list <python:list>` of :class:`str <python:str>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`Geography`

        """
        csv_record = validators.iterable(csv_record, allow_empty = False)

        coordinates = csv_record[5].split(',')
        longitude = coordinates[0]
        latitude = coordinates[1]

        state_fips_code = csv_record[8]
        county_fips_code = csv_record[9]
        tract = csv_record[10]
        block = csv_record[11]

        return cls(state_fips_code = state_fips_code,
                   county_fips_code = county_fips_code,
                   tract = tract,
                   block = block,
                   longitude = longitude,
                   latitute = latitude)

    @classmethod
    def from_dict(cls, as_dict):
        geoid = as_dict.pop('GEOID', None)
        oid = as_dict.pop('OID', None)
        object_id = as_dict.pop('OBJECTID', None)
        name = as_dict.pop('NAME', None)
        basename = as_dict.pop('BASENAME', name)
        funcstat = as_dict.pop('FUNCSTAT', None)
        lsad = as_dict.pop('LSAD', None)
        legislative_session_year = as_dict.pop('LSY', None)

        state_fips_code = as_dict.pop('STATE', None)
        state_ns = as_dict.pop('STATENS', None)
        state_abbreviation = as_dict.pop('STUSAB', None)

        division_fips_code = as_dict.pop('DIVISION', None)
        region_fips_code = as_dict.pop('REGION', None)

        tract = as_dict.pop('TRACT', None)
        block = as_dict.pop('BLOCK', None)
        block_group = as_dict.pop('BLKGRP', None)

        county_fips_code = as_dict.pop('COUNTY', None)
        county_cc = as_dict.pop('COUNTYCC', None)
        county_ns = as_dict.pop('COUNTYNS', None)

        place = as_dict.pop('PLACE', None)
        place_cc = as_dict.pop('PLACECC', None)
        place_ns = as_dict.pop('PLACENS', None)

        necta_pci = as_dict.pop('NECTAPCI', None)
        cbsa_pci = as_dict.pop('CBSAPCI', None)

        congressional_session_code = as_dict.pop('CDSESSN', None)

        zcta5 = as_dict.pop('ZCTA5', None)
        zcta5_cc = as_dict.pop('ZCTA5CC', None)

        school_district_type = as_dict.pop('SDTYP', None)
        low_school_grade = as_dict.pop('LOGRADE', None)
        high_school_grade = as_dict.pop('HIGRADE', None)

        csa = as_dict.pop('CSA', None)
        cbsa = as_dict.pop('CBSA', None)

        longitude = as_dict.pop('CENTLON', None)
        latitude = as_dict.pop('CENTLAT', None)
        longitude_internal_point = as_dict.pop('INTPTLON', None)
        latitude_internal_point = as_dict.pop('INTPTLAT', None)

        water_area = as_dict.pop('AREAWATER', None)
        land_area = as_dict.pop('AREALAND', None)

        return cls(geoid = geoid,
                   oid = oid,
                   object_id = object_id,
                   name = name,
                   basename = basename,
                   funcstat = funcstat,
                   lsad = lsad,
                   legislative_session_year = legislative_session_year,
                   state_fips_code = state_fips_code,
                   state_ns = state_ns,
                   state_abbreviation = state_abbreviation,
                   division_fips_code = division_fips_code,
                   region_fips_code = region_fips_code,
                   tract = tract,
                   block = block,
                   block_group = block_group,
                   county_fips_code = county_fips_code,
                   county_cc = county_cc,
                   county_ns = county_ns,
                   place = place,
                   place_cc = place_cc,
                   place_ns = place_ns,
                   necta_pci = necta_pci,
                   cbsa_pci = cbsa_pci,
                   congressional_session_code = congressional_session_code,
                   zcta5 = zcta5,
                   zcta5_cc = zcta5_cc,
                   school_district_type = school_district_type,
                   low_school_grade = low_school_grade,
                   high_school_grade = high_school_grade,
                   csa = csa,
                   cbsa = cbsa,
                   longitude = longitude,
                   latitude = latitude,
                   longitude_internal_point = longitude_internal_point,
                   latitude_internal_point = latitude_internal_point,
                   water_area = water_area,
                   land_area = land_area,
                   **as_dict)

    def to_dict(self):
        """Returns a :class:`dict <python:dict>` representation of the geographic entity.

        .. note::

          The :class:`dict <python:dict>` representation matches the JSON structure for
          the US Census Geocoder API. This is a not-very-pythonic
          :class:`dict <python:dict>` structure, but at least this ensures idempotency.

        .. warning::

          Note that certain geography types only use a subset of the properties returned.
          Unused or unavailable properties will be returned as :obj:`None <python:None>`
          which will be converted to ``null`` if serialized to JSON.

        :returns: :class:`dict <python:dict>` representation of the entity.
        :rtype: :class:`dict <python:dict>`
        """
        result = {
            'GEOID': self.geoid,
            'OID': self.oid,
            'OBJECT_ID': self.object_id,
            'NAME': self.name,
            'BASENAME': self.basename,
            'FUNCSTAT': self.funcstat,
            'LSAD': self.lsad,
            'LSY': self.lsy,
            'STATE': self.state_fips_code,
            'STATE_NS': self.state_ns,
            'STUSAB': self.state_abbreviation,
            'DIVISION': self.division_fips_code,
            'REGION': self.region_fips_code,
            'TRACT': self.tract,
            'BLOCK': self.block,
            'BLKGRP': self.block_group,
            'COUNTY': self.county_fips_code,
            'COUNTYCC': self.county_cc,
            'COUNTYNS': self.county_ns,
            'PLACE': self.place,
            'PLACECC': self.place_cc,
            'PLACENS': self.place_ns,
            'NECTAPCI': self.necta_pci,
            'CBSAPCI': self.cbsa_pci,
            'CDSESSN': self.congressional_session_code,
            'ZCTA5': self.zcta5,
            'ZCTA5CC': self.zcta5_cc,
            'SDTYP': self.school_district_type,
            'LOGRADE': self.low_school_grade,
            'HIGRADE': self.high_school_grade,
            'CSA': self.csa,
            'CBSA': self.cbsa,
            'AREAWATER': self.water_area,
            'AREALAND': self.land_area
        }
        if self.longitude:
            if self.longitude >= 0:
                prefix = '+'
            else:
                prefix = ''
            result['CENTLON'] = f'{prefix}{self.longitude:.8f}'
        if self.latitude:
            if self.latitude >= 0:
                prefix = '+'
            else:
                prefix = ''
            result['CENTLAT'] = f'{prefix}{self.latitude:.8f}'
        if self.longitude_internal_point:
            if self.longitude_internal_point >= 0:
                prefix = '+'
            else:
                prefix = ''
            result['INTPTLON'] = f'{prefix}{self.longitude_internal_point:.8f}'
        if self.latitude_internal_point:
            if self.latitude_internal_point >= 0:
                prefix = '+'
            else:
                prefix = ''
            result['INTPTLAT'] = f'{prefix}{self.latitude_internal_point:.8f}'

        for key in self.extensions:
            result[key] = self.extensions.get(key)

        return result

    def inspect(self, as_census_fields = False):
        """Produce a list of the geographic area's properties that have values.

        :param as_census_fields: If ``True``, return property names as they appear in
          Census databases or the output of the `Census Geocoder API`_. If ``False``,
          return properties as they are defined on the **Census Geocoder** objects.
          Defaults to ``False``.
        :type as_census_fields: :class:`bool <python:bool>`

        :rtype: :class:`list <python:list>` of :class:`str <python:str>`
        """
        result = []

        if self.geoid and as_census_fields:
            result.append('GEOID')
        elif self.geoid:
            result.append('geoid')

        if self.oid and as_census_fields:
            result.append('OID')
        elif self.oid:
            result.append('oid')

        if self.object_id and as_census_fields:
            result.append('OBJECTID')
        elif self.object_id:
            result.append('object_id')

        if self.name and as_census_fields:
            result.append('NAME')
        elif self.name:
            result.append('name')
        if self.basename and as_census_fields:
            result.append('BASENAME')
        elif self.basename:
            result.append('basename')

        if self.funcstat and as_census_fields:
            result.append('FUNCSTAT')
        elif self.funcstat:
            result.append('funcstat')
        if self.functional_status and not as_census_fields:
            result.append('functional_status')

        if self.lsad and as_census_fields:
            result.append('LSAD')
        elif self.lsad:
            result.append('lsad')
        if self.legal_statistical_area and not as_census_fields:
            result.append('legal_statistical_area')
        if self.lsad_category and not as_census_fields:
            result.append('lsad_category')

        if self.legislative_session_year and as_census_fields:
            result.append('LSY')
        elif self.legislative_session_year:
            result.append('legislative_session_year')

        if self.state_fips_code and as_census_fields:
            result.append('STATE')
        elif self.state_fips_code:
            result.append('state_fips_code')
        if self.state_ns and as_census_fields:
            result.append('STATENS')
        elif self.state_ns:
            result.append('state_ns')
        if self.state_abbreviation and as_census_fields:
            result.append('STUSAB')
        elif self.state_abbreviation:
            result.append('state_abbreviation')

        if self.division_fips_code and as_census_fields:
            result.append('DIVISION')
        elif self.division_fips_code:
            result.append('division_fips_code')
        if self.region_fips_code and as_census_fields:
            result.append('REGION')
        elif self.region_fips_code:
            result.append('region_fips_code')

        if self.tract and as_census_fields:
            result.append('TRACT')
        elif self.tract:
            result.append('tract')
        if self.block and as_census_fields:
            result.append('BLOCK')
        elif self.block:
            result.append('block')
        if self.block_group and as_census_fields:
            result.append('BLKGRP')
        elif self.block_group:
            result.append('block_group')

        if self.county_fips_code and as_census_fields:
            result.append('COUNTY')
        elif self.county_fips_code:
            result.append('county_fips_code')
        if self.county_ns and as_census_fields:
            result.append('COUNTYNS')
        elif self.county_ns:
            result.append('county_ns')
        if self.county_cc and as_census_fields:
            result.append('COUNTYCC')
        elif self.county_cc:
            result.append('county_cc')

        if self.place_fips_code and as_census_fields:
            result.append('PLACE')
        elif self.place_fips_code:
            result.append('place_fips_code')
        if self.place_ns and as_census_fields:
            result.append('PLACENS')
        elif self.place_ns:
            result.append('place_ns')
        if self.place_cc and as_census_fields:
            result.append('PLACECC')
        elif self.place_cc:
            result.append('place_cc')

        if self.necta_pci and as_census_fields:
            result.append('NECTAPCI')
        elif self.necta_pci:
            result.append('necta_pci')
        if self.cbsa_pci and as_census_fields:
            result.append('CBSAPCI')
        elif self.cbsa_pci:
            result.append('cbsa_pci')

        if self.congressional_session_code and as_census_fields:
            result.append('CDSESSN')
        elif self.congressional_session_code:
            result.append('congressional_session_code')

        if self.zcta5 and as_census_fields:
            result.append('ZCTA5')
        elif self.zcta5:
            result.append('zcta5')
        if self.zcta5_cc and as_census_fields:
            result.append('ZCTA5CC')
        elif self.zcta5_cc:
            result.append('zcta5_cc')

        if self.school_district_type and as_census_fields:
            result.append('SDTYP')
        elif self.school_district_type:
            result.append('school_district_type')
        if self.low_school_grade and as_census_fields:
            result.append('LOGRADE')
        elif self.low_school_grade:
            result.append('low_school_grade')
        if self.high_school_grade and as_census_fields:
            result.append('HIGRADE')
        elif self.high_school_grade:
            result.append('high_school_grade')

        if self.csa and as_census_fields:
            result.append('CSA')
        elif self.csa:
            result.append('csa')
        if self.cbsa and as_census_fields:
            result.append('CBSA')
        elif self.cbsa:
            result.append('cbsa')

        if self.longitude and as_census_fields:
            result.append('CENTLON')
        elif self.longitude:
            result.append('longitude')
        if self.latitude and as_census_fields:
            result.append('CENTLAT')
        elif self.latitude:
            result.append('latitude')
        if self.longitude_internal_point and as_census_fields:
            result.append('INTPTLON')
        elif self.longitude_internal_point:
            result.append('longitude_internal_point')
        if self.latitude_internal_point and as_census_fields:
            result.append('INTPTLAT')
        elif self.latitude_internal_point:
            result.append('latitude_internal_point')

        if self.water_area and as_census_fields:
            result.append('AREAWATER')
        elif self.water_area:
            result.append('water_area')
        if self.land_area and as_census_fields:
            result.append('AREALAND')
        elif self.land_area:
            result.append('land_area')

        return result


class PUMA(GeographicArea):
    """Public Use Microdata Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Public Use Microdata Area'


class PUMA_2010(PUMA):
    """2010 Census Public Use Microdata Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2010 Census Public Use Microdata Area'


class StateLegislativeDistrictLower(GeographicArea):
    """State Legislative District - Lower"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'State Legislative District - Lower'


class StateLegislativeDistrictUpper(GeographicArea):
    """State Legislative District - Upper"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'State Legislative District - Upper'


class StateLegislativeDistrictLower_2018(StateLegislativeDistrictLower):
    """2018 State Legislative District - Lower"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2018 State Legislative District - Lower'


class StateLegislativeDistrictUpper_2018(StateLegislativeDistrictUpper):
    """2018 State Legislative District - Upper"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2018 State Legislative District - Upper'


class StateLegislativeDistrictLower_2016(StateLegislativeDistrictLower):
    """2016 State Legislative District - Lower"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2016 State Legislative District - Lower'


class StateLegislativeDistrictUpper_2016(StateLegislativeDistrictUpper):
    """2016 State Legislative District - Upper"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2016 State Legislative District - Upper'


class StateLegislativeDistrictLower_2012(StateLegislativeDistrictLower):
    """2012 State Legislative District - Lower"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2012 State Legislative District - Lower'


class StateLegislativeDistrictUpper_2012(StateLegislativeDistrictUpper):
    """2012 State Legislative District - Upper"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2012 State Legislative District - Upper'


class StateLegislativeDistrictLower_2010(StateLegislativeDistrictLower):
    """2010 State Legislative District - Lower"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2010 State Legislative District - Lower'


class StateLegislativeDistrictUpper_2010(StateLegislativeDistrictUpper):
    """2010 State Legislative District - Upper"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2010 State Legislative District - Upper'


class County(GeographicArea):
    """County"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'County'


class ZCTA5(GeographicArea):
    """ZCTA5"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Zip Code Tabulation Area'


class ZCTA_2010(ZCTA5):
    """2010 Zip Code Tabulation Areas"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2010 Census ZIP Code Tabulation Area'


class ZCTA_2020(ZCTA5):
    """2020 Zip Code Tabulation Areas"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2020 Census ZIP Code Tabulation Area'


class UnifiedSchoolDistrict(GeographicArea):
    """Unified School District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Unified School District'


class SecondarySchoolDistrict(GeographicArea):
    """Secondary School District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Secondary School District'


class ElementarySchoolDistrict(GeographicArea):
    """Elementary School District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Elementary School District'


class VotingDistrict(GeographicArea):
    """Voting District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'County'


class MetropolitanDivision(GeographicArea):
    """Metropolitan Division"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Metropolitan Division'


class State(GeographicArea):
    """State"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'State'


class CensusBlockGroup(GeographicArea):
    """Census Block Group"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Census Block Group'


class TribalCensusBlockGroup(CensusBlockGroup):
    """Tribal Census Block Group"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Tribal Census Block Group'


class CombinedStatisticalArea(GeographicArea):
    """Combined Statistical Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Combined Statistical Area'


class CountySubDivision(GeographicArea):
    """County Sub-division"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'County Sub-division'


class TribalSubDivision(GeographicArea):
    """Tribal Sub-division"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Tribal Sub-division'


class CensusDesignatedPlace(GeographicArea):
    """Census Designated Place"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Census Designated Place'


class CensusDivision(GeographicArea):
    """Census Division"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Division'


class CongressionalDistrict(GeographicArea):
    """Congressional District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Congressional District'


class CongressionalDistrict_116(CongressionalDistrict):
    """116th Congressional District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '116th Congressional District'


class CongressionalDistrict_115(CongressionalDistrict):
    """115th Congressional District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '115th Congressional District'


class CongressionalDistrict_113(CongressionalDistrict):
    """113th Congressional District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '113th Congressional District'


class CongressionalDistrict_111(CongressionalDistrict):
    """111th Congressional District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '111th Congressional District'


class CensusRegion(GeographicArea):
    """Census Region"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Region'


class MetropolitanStatisticalArea(GeographicArea):
    """Metropolitan Statistical Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Metropolitan Statistical Area'


class MicropolitanStatisticalArea(GeographicArea):
    """Micropolitan Statistical Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Micropolitan Statistical Area'


class CensusBlock(GeographicArea):
    """Census Block"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Census Block'


class CensusBlock_2020(CensusBlock):
    """2020 Census Blocks"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2020 Census Block'


class CensusTract(GeographicArea):
    """Census Tract"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Census Tract'


class TribalCensusTract(CensusTract):
    """Tribal Census Tract"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Tribal Census Tract'


class Estate(GeographicArea):
    """Estate"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Estate'


class Subbarrio(GeographicArea):
    """Subbarrio"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Subbarrio'


class ConsolidatedCity(GeographicArea):
    """Consolidated City"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Consolidated City'


class IncorporatedPlace(GeographicArea):
    """Incorporated Place"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Incorporated Place'


class ANRC(GeographicArea):
    """Alaska Native Regional Corporation"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Alaska Native Regional Corporation'


class FederalAmericanIndianReservation(GeographicArea):
    """Federal American Indian Reservation"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Federal American Indian Reservation'


class OffReservationTrustLand(GeographicArea):
    """Off-Reservation Trust Land"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Off-Reservation Trust Land'


class StateAmericanIndianReservation(GeographicArea):
    """State American Indian Reservation"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'State American Indian Reservation'


class HawaiianHomeLand(GeographicArea):
    """Hawaiian Home Land"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Hawaiian Home Land'


class ANVSA(GeographicArea):
    """Alaska Native Village Statistical Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Alaska Native Village Statistical Area'


class OTSA(GeographicArea):
    """Oklahoma Tribal Statistical Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Oklahoma Tribal Statistical Area'


class SDTSA(GeographicArea):
    """State Designated Tribal Statistical Areas"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'State Designated Tribal Statistical Area'


class TDSA(GeographicArea):
    """Tribal Designated Statistical Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Tribal Designated Statistical Area'


class AIJUA(GeographicArea):
    """American Indian Joint-Use Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'American Indian Joint-Use Area'


class CombinedNECTA(GeographicArea):
    """Combined New England City and Town Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Combined New England City and Town Area'


class NECTADivision(GeographicArea):
    """New England City and Town Area Division"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'New England City and Town Area Division'


class MetropolitanNECTA(CombinedNECTA):
    """Metropolitan New England City and Town Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Metropolitan New England City and Town Area'


class MicropolitanNECTA(CombinedNECTA):
    """Micropolitan New England City and Town Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Micropolitan New England City and Town Area'


class UrbanGrowthArea(GeographicArea):
    """Urban Growth Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Urban Growth Area'


class UrbanizedArea(GeographicArea):
    """Urbanized Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Urbanized Area'


class UrbanCluster(GeographicArea):
    """Urban Cluster"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Urban Cluster'


class UrbanizedArea_2010(UrbanizedArea):
    """2010 Census Urbanized Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2010 Census Urbanized Area'


class UrbanCluster_2010(UrbanCluster):
    """2010 Census Urban Cluster"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return '2010 Census Urban Cluster'


class TrafficAnalysisDistrict(GeographicArea):
    """Traffic Analysis District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Traffic Analysis District'


class TrafficAnalysisZone(GeographicArea):
    """Traffic Analysis Zone"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Traffic Analysis Zone'


# Key represents the ``geography_type`` returned by the Census Geocoder API.
# Tuple contains the GeographyCollection property name and the GeographicArea sub-class.
GEOGRAPHY_MAP = {
    '2010 Census Public Use Microdata Areas': ('pumas_2010', PUMA_2010),
    'Public Use Microdata Areas': ('pumas', PUMA),
    'Census Regions': ('regions', CensusRegion),
    'Census Divisions': ('divisions', CensusDivision),
    'States': ('states', State),
    'Counties': ('counties', County),
    'County Subdivisions': ('county_subdivisions', CountySubDivision),
    'Tribal Subdivisions': ('tribal_subdivisions', TribalSubDivision),
    'Metropolitan Divisions': ('metropolitan_divisions', MetropolitanDivision),
    '2010 Census ZIP Code Tabulation Areas': ('zcta_2010', ZCTA_2010),
    '2020 ZIP code Tabulation Areas': ('zcta_2020', ZCTA_2020),
    'ZIP Code Tabulation Areas': ('zcta5', ZCTA5),
    'Zip Code Tabulation Areas': ('zcta5', ZCTA5),
    'Unified School Districts': ('unified_school_districts', UnifiedSchoolDistrict),
    'Secondary School Districts': ('secondary_school_districts', SecondarySchoolDistrict),
    'Elementary School Districts': ('elementary_school_districts',
                                    ElementarySchoolDistrict),
    'Voting Districts': ('voting_districts', VotingDistrict),
    'State Legislative Districts - Upper': ('state_legislative_districts_upper',
                                            StateLegislativeDistrictUpper),
    'State Legislative Districts - Lower': ('state_legislative_districts_lower',
                                            StateLegislativeDistrictLower),
    '2018 State Legislative Districts - Upper': ('state_legislative_districts_upper_2018',
                                                 StateLegislativeDistrictUpper_2018),
    '2018 State Legislative Districts - Lower': ('state_legislative_districts_lower_2018',
                                                 StateLegislativeDistrictLower_2018),
    '2016 State Legislative Districts - Upper': ('state_legislative_districts_upper_2016',
                                                 StateLegislativeDistrictUpper_2016),
    '2016 State Legislative Districts - Lower': ('state_legislative_districts_lower_2016',
                                                 StateLegislativeDistrictLower_2016),
    '2012 State Legislative Districts - Upper': ('state_legislative_districts_upper_2012',
                                                 StateLegislativeDistrictUpper_2012),
    '2012 State Legislative Districts - Lower': ('state_legislative_districts_lower_2012',
                                                 StateLegislativeDistrictLower_2012),
    '2010 State Legislative Districts - Upper': ('state_legislative_districts_upper_2010',
                                                 StateLegislativeDistrictUpper_2010),
    '2010 State Legislative Districts - Lower': ('state_legislative_districts_lower_2010',
                                                 StateLegislativeDistrictLower_2010),
    '116th Congressional Districts': ('congressional_districts_116',
                                      CongressionalDistrict_116),
    '115th Congressional Districts': ('congressional_districts_115',
                                      CongressionalDistrict_115),
    '113th Congressional Districts': ('congressional_districts_113',
                                      CongressionalDistrict_113),
    '111th Congressional Districts': ('congressional_districts_111',
                                      CongressionalDistrict_111),
    'Combined Statistical Areas': ('csa', CombinedStatisticalArea),
    'Metropolitan Statistical Areas': ('msa', MetropolitanStatisticalArea),
    'Micropolitan Statistical Areas': ('micropolitan_stastistical_areas',
                                       MicropolitanStatisticalArea),
    'Census Block Groups': ('block_groups', CensusBlockGroup),
    'Tribal Census Block Groups': ('tribal_block_groups', TribalCensusBlockGroup),
    'Census Blocks': ('blocks', CensusBlock),
    '2020 Census Blocks': ('blocks_2020', CensusBlock_2020),
    'Tribal Census Tracts': ('tribal_tracts', TribalCensusTract),
    'Census Tracts': ('tracts', CensusTract),
    'Census Designated Places': ('metrpolitan_nectas', CensusDesignatedPlace),
    'Estates': ('estates', Estate),
    'Subbarrios': ('subbarrios', Subbarrio),
    'Consolidated Cities': ('consolidated_cities', ConsolidatedCity),
    'Incorporated Places': ('incorporated_places', IncorporatedPlace),
    'Alaska Native Regional Corporations': ('anrc', ANRC),
    'Federal American Indian Reservations': ('federal_american_indian_reservations',
                                             FederalAmericanIndianReservation),
    'Off-Reservation Trust Lands': ('off_reservation_trust_lands',
                                    OffReservationTrustLand),
    'State American Indian Reservations': ('state_american_indian_reservations',
                                           StateAmericanIndianReservation),
    'Hawaiian Home Lands': ('hawaiian_home_lands', HawaiianHomeLand),
    'Alaska Native Village Statistical Areas': ('anvsa', ANVSA),
    'Oklahoma Tribal Statistical Areas': ('otsa', OTSA),
    'State Designated Tribal Statistical Areas': ('sdtsa', SDTSA),
    'Tribal Designated Statistical Areas': ('tdsa', TDSA),
    'American Indian Joint-Use Areas': ('american_indian_joint_use_areas', AIJUA),
    'Combined New England City and Town Areas': ('combined_nectas', CombinedNECTA),
    'New England City and Town Area Divisions': ('necta_divisions', NECTADivision),
    'Metropolitan New England City and Town Areas': ('metropolitan_nectas',
                                                     MetropolitanNECTA),
    'Micopolitan New England City and Town Areas': ('micropolitan_nectas',
                                                    MicropolitanNECTA),
    'Urban Growth Areas': ('urban_growth_areas', UrbanGrowthArea),
    'Urbanized Areas': ('urbanized_areas', UrbanizedArea),
    '2010 Census Urbanized Areas': ('urbanized_areas_2010', UrbanizedArea_2010),
    'Urban Clusters': ('urban_clusters', UrbanCluster),
    '2010 Census Urban Clusters': ('urban_clusters_2010', UrbanCluster_2010),
    'Traffic Analysis Districts': ('traffic_analysis_districts', TrafficAnalysisDistrict),
    'Traffic Analysis Zones': ('traffic_analysis_zones', TrafficAnalysisZone),
}


def get_target_layer_cls(property_name):
    """Return the :class:`GeographicArea` sub-class that corresponds to ``proprety_name``.

    :param property_name: The :class:`GeographyCollection` property name whose
      correpsonding :class:`GeographicArea` sub-class should be returned.
    :type property_name: :class:`str <python:str>`

    :returns: A sub-class of :class:`GeographicArea`
    :rtype: class object of :class:`GeographicArea`

    """
    for key in GEOGRAPHY_MAP:
        tuple_object = GEOGRAPHY_MAP.get(key, None)
        if tuple_object and tuple_object[0] == property_name:
            return tuple_object[1]

    raise errors.CensusGeocoderError(f'Property name "{property_name}" not recognized.')


def validate_layer_values(value, property_name):
    """Ensure that ``value`` is an iterable of :class:`GeographicArea`.

    :param value: The value to validate.
    :type value: iterable of :class:`GeographicArea` or :class:`dict <python:dict>`

    :param property_name: The name of the property that is being populated.
    :type property_name: :class:`str <python:str>`

    :returns: Collection of :class:`GeographicArea` instances
    :rtype: iterable of :class:`GeographicArea`
    """
    value = validators.iterable(value, allow_empty = False)
    target_cls = get_target_layer_cls(property_name)
    validated_values = []
    for item in value:
        if not isinstance(item, target_cls):
            item = validators.dict(value, allow_empty = False)
            validated_value = target_cls.from_dict(item)
            validated_values.append(validated_value)
        else:
            validated_values.append(item)

    return validated_values


LAYER_PROPERTIES = [GEOGRAPHY_MAP.get(x)[0] for x in GEOGRAPHY_MAP]


class GeographyCollection(metaclasses.BaseEntity):
    """Collection of :class:`GeographicArea` objects."""

    def __init__(self, **kwargs):
        self._pumas_2010 = []
        self._pumas = []
        self._regions = []
        self._divisions = []
        self._states = []
        self._counties = []
        self._county_subdivisions = []
        self._tribal_subdivisions = []
        self._metropolitan_divisions = []
        self._zcta5 = []
        self._zcta_2020 = []
        self._zcta_2010 = []
        self._unified_school_districts = []
        self._secondary_school_districts = []
        self._elementary_school_districts = []
        self._voting_districts = []
        self._state_legislative_districts_upper = []
        self._state_legislative_districts_lower = []
        self._state_legislative_districts_upper_2018 = []
        self._state_legislative_districts_lower_2018 = []
        self._state_legislative_districts_upper_2016 = []
        self._state_legislative_districts_lower_2016 = []
        self._state_legislative_districts_upper_2012 = []
        self._state_legislative_districts_lower_2012 = []
        self._state_legislative_districts_upper_2010 = []
        self._state_legislative_districts_lower_2010 = []
        self._congressional_districts_116 = []
        self._congressional_districts_115 = []
        self._congressional_districts_113 = []
        self._congressional_districts_111 = []
        self._csa = []
        self._msa = []
        self._block_groups = []
        self._blocks = []
        self._blocks_2020 = []
        self._tracts = []
        self._tribal_tracts = []
        self._tribal_block_groups = []
        self._metrpolitan_nectas = []
        self._estates = []
        self._subbarrios = []
        self._consolidated_cities = []
        self._incorporated_places = []
        self._anrc = []
        self._federal_american_indian_reservations = []
        self._off_reservation_trust_lands = []
        self._state_american_indian_reservations = []
        self._hawaiian_home_lands = []
        self._anvsa = []
        self._otsa = []
        self._sdtsa = []
        self._tdsa = []
        self._american_indian_joint_use_areas = []
        self._combined_nectas = []
        self._necta_divisions = []
        self._metropolitan_nectas = []
        self._micropolitan_nectas = []
        self._urban_growth_areas = []
        self._urbanized_areas = []
        self._urbanized_areas_2010 = []
        self._urban_clusters = []
        self._urban_clusters_2010 = []
        self._traffic_analysis_districts = []
        self._traffic_analysis_zones = []

        if kwargs:
            self = self.from_dict(kwargs)

    def __len__(self):
        cls = self.__class__
        potential_properties = [x for x in dir(cls)
                                if not x.startswith('_')]
        result = 0
        for item in potential_properties:
            if checkers.is_type(getattr(cls, item), 'property'):
                result += len(getattr(self, item))

        return result

    def _set_hidden_property(self, value, property_name):
        """Validates ``value`` and sets the correpsonding hidden property for the
        indicated layer.

        :param values: The values to validate / set.
        :type values: iterable

        :param property_name: The original property name is being set.
        :type property_name: :class:`str <python:str>`

        """
        values = validate_layer_values(value, property_name)
        attr_target = f'_{property_name}'

        if not values:
            setattr(self, attr_target, [])
        else:
            setattr(self, attr_target, [x for x in values])

    @property
    def pumas_2010(self):
        """2010 Census Public Use Microdata Areas

        :rtype: :class:`list <python:list>` of :class:`PUMA_2010`
        """
        return self._pumas_2010

    @pumas_2010.setter
    def pumas_2010(self, value):
        property_name = currentframe().f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def pumas(self):
        """Public Use Microdata Areas

        :rtype: :class:`list <python:list>` of :class:`PUMA`
        """
        return self._pumas

    @pumas.setter
    def pumas(self, value):
        property_name = currentframe().f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def regions(self):
        """Census Regions

        :rtype: :class:`list <python:list>` of :class:`CensusRegion`
        """
        return self._regions

    @regions.setter
    def regions(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def divisions(self):
        """Census Divisions

        :rtype: :class:`list <python:list>` of :class:`CensusDivision`
        """
        return self._divisions

    @divisions.setter
    def divisions(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def states(self):
        """States

        :rtype: :class:`list <python:list>` of :class:`State`
        """
        return self._states

    @states.setter
    def states(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def counties(self):
        """Census Counties

        :rtype: :class:`list <python:list>` of :class:`County`
        """
        return self._counties

    @counties.setter
    def counties(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def county_subdivisions(self):
        """County Sub-division

        :rtype: :class:`list <python:list>` of :class:`CountySubDivision`
        """
        return self._county_subdivisions

    @county_subdivisions.setter
    def county_subdivisions(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def tribal_subdivisions(self):
        """Tribal Sub-divisions

        :rtype: :class:`list <python:list>` of :class:`TribalSubDivision`
        """
        return self._tribal_subdivisions

    @tribal_subdivisions.setter
    def tribal_subdivisions(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def metropolitan_divisions(self):
        """Metropolitan Divisions

        :rtype: :class:`list <python:list>` of :class:`MetropolitanDivision`
        """
        return self._metropolitan_divisions

    @metropolitan_divisions.setter
    def metropolitan_divisions(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def zcta_2010(self):
        """2010 Census ZIP Code Tabulation Areas

        :rtype: :class:`list <python:list>` of :class:`ZCTA_2010`
        """
        return self._zcta_2010

    @zcta_2010.setter
    def zcta_2010(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def zcta_2020(self):
        """2020 Census ZIP Code Tabulation Areas

        :rtype: :class:`list <python:list>` of :class:`ZCTA_2020`
        """
        return self._zcta_2020

    @zcta_2020.setter
    def zcta_2020(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def zcta5(self):
        """Zip Code Tabulation Area

        :rtype: :class:`list <python:list>` of :class:`ZCTA5`
        """
        return self._zcta5

    @zcta5.setter
    def zcta5(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def unified_school_districts(self):
        """Unified School Districts

        :rtype: :class:`list <python:list>` of :class:`UnifiedSchoolDistrict`
        """
        return self._unified_school_districts

    @unified_school_districts.setter
    def unified_school_districts(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def secondary_school_districts(self):
        """Secondary School Districts

        :rtype: :class:`list <python:list>` of :class:`SecondarySchoolDistrict`
        """
        return self._secondary_school_districts

    @secondary_school_districts.setter
    def secondary_school_districts(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def elementary_school_districts(self):
        """Elementary School Districts

        :rtype: :class:`list <python:list>` of :class:`ElementarySchoolDistrict`
        """
        return self._elementary_school_districts

    @elementary_school_districts.setter
    def elementary_school_districts(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def voting_districts(self):
        """Voting Districts

        :rtype: :class:`list <python:list>` of :class:`VotingDistrict`
        """
        return self._voting_districts

    @voting_districts.setter
    def voting_districts(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_upper(self):
        """State Legislative Districts - Upper

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictUpper`
        """
        return self._state_legislative_districts_upper

    @state_legislative_districts_upper.setter
    def state_legislative_districts_upper(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_lower(self):
        """State Legislative Districts - Lower

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictLower`
        """
        return self._state_legislative_districts_lower

    @state_legislative_districts_lower.setter
    def state_legislative_districts_lower(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_upper_2018(self):
        """2018 State Legislative Districts - Upper

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictUpper_2018`
        """
        return self._state_legislative_districts_upper_2018

    @state_legislative_districts_upper_2018.setter
    def state_legislative_districts_upper(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_lower_2018(self):
        """2018 State Legislative Districts - Lower

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictLower_2018`
        """
        return self._state_legislative_districts_lower_2018

    @state_legislative_districts_lower_2018.setter
    def state_legislative_districts_lower_2018(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_upper_2016(self):
        """2016 State Legislative Districts - Upper

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictUpper_2016`
        """
        return self._state_legislative_districts_upper_2016

    @state_legislative_districts_upper_2016.setter
    def state_legislative_districts_upper(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_lower_2016(self):
        """2016 State Legislative Districts - Lower

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictLower_2016`
        """
        return self._state_legislative_districts_lower_2016

    @state_legislative_districts_lower_2016.setter
    def state_legislative_districts_lower_2016(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_upper_2012(self):
        """2012 State Legislative Districts - Upper

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictUpper_2012`
        """
        return self._state_legislative_districts_upper_2012

    @state_legislative_districts_upper_2012.setter
    def state_legislative_districts_upper(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_lower_2012(self):
        """2012 State Legislative Districts - Lower

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictLower_2012`
        """
        return self._state_legislative_districts_lower_2012

    @state_legislative_districts_lower_2012.setter
    def state_legislative_districts_lower_2012(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_upper_2010(self):
        """2010 State Legislative Districts - Upper

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictUpper_2010`
        """
        return self._state_legislative_districts_upper_2010

    @state_legislative_districts_upper_2010.setter
    def state_legislative_districts_upper(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_legislative_districts_lower_2010(self):
        """2010 State Legislative Districts - Lower

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictLower_2010`
        """
        return self._state_legislative_districts_lower_2010

    @state_legislative_districts_lower_2010.setter
    def state_legislative_districts_lower_2010(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def congressional_districts_116(self):
        """116th Congressional Districts

        :rtype: :class:`list <python:list>` of :class:`CongressionalDistrict_116`
        """
        return self._congressional_districts_116

    @congressional_districts_116.setter
    def congressional_districts_116(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def congressional_districts_115(self):
        """115th Congressional Districts

        :rtype: :class:`list <python:list>` of :class:`CongressionalDistrict_115`
        """
        return self._congressional_districts_115

    @congressional_districts_115.setter
    def congressional_districts_115(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def congressional_districts_113(self):
        """113th Congressional Districts

        :rtype: :class:`list <python:list>` of :class:`CongressionalDistrict_113`
        """
        return self._congressional_districts_113

    @congressional_districts_113.setter
    def congressional_districts_113(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def congressional_districts_111(self):
        """111th Congressional Districts

        :rtype: :class:`list <python:list>` of :class:`CongressionalDistrict_111`
        """
        return self._congressional_districts_111

    @congressional_districts_111.setter
    def congressional_districts_111(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def csa(self):
        """Combined Statistical Areas

        :rtype: :class:`list <python:list>` of :class:`CombinedStatisticalArea`
        """
        return self._csa

    @csa.setter
    def csa(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def msa(self):
        """Metropolitan Statistical Area

        :rtype: :class:`list <python:list>` of :class:`MetropolitanStatisticalArea`
        """
        return self._msa

    @msa.setter
    def msa(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def block_groups(self):
        """Census Block Groups

        :rtype: :class:`list <python:list>` of :class:`CensusBlockGroup`
        """
        return self._block_groups

    @block_groups.setter
    def block_groups(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def tribal_block_groups(self):
        """Tribal Census Block Groups

        :rtype: :class:`list <python:list>` of :class:`TribalCensusBlockGroup`
        """
        return self._tribal_block_groups

    @tribal_block_groups.setter
    def tribal_block_groups(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def blocks(self):
        """Census Blocks

        :rtype: :class:`list <python:list>` of :class:`CensusBlock`
        """
        return self._blocks

    @blocks.setter
    def blocks(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def blocks_2020(self):
        """2020 Census Blocks

        :rtype: :class:`list <python:list>` of :class:`CensusBlock_2020`
        """
        return self._blocks

    @blocks_2020.setter
    def blocks_2020(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def tracts(self):
        """Census Tracts

        :rtype: :class:`list <python:list>` of :class:`CensusTract`
        """
        return self._tracts

    @tracts.setter
    def tracts(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def tribal_tracts(self):
        """Tribal Census Tracts

        :rtype: :class:`list <python:list>` of :class:`TribalCensusTract`
        """
        return self._tribal_tracts

    @tribal_tracts.setter
    def tribal_tracts(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def metrpolitan_nectas(self):
        """Census Designated Places

        :rtype: :class:`list <python:list>` of :class:`CensusDesignatedPlace`
        """
        return self._metrpolitan_nectas

    @metrpolitan_nectas.setter
    def metrpolitan_nectas(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def estates(self):
        """Estates

        :rtype: :class:`list <python:list>` of :class:`Estate`
        """
        return self._estates

    @estates.setter
    def estates(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def subbarrios(self):
        """Sub-barrios

        :rtype: :class:`list <python:list>` of :class:`Subbarrio`
        """
        return self._subbarrios

    @subbarrios.setter
    def subbarrios(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def consolidated_cities(self):
        """Consolidated Cities

        :rtype: :class:`list <python:list>` of :class:`ConsolidatedCity`
        """
        return self._consolidated_cities

    @consolidated_cities.setter
    def consolidated_cities(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def incorporated_places(self):
        """Incorporated Places

        :rtype: :class:`list <python:list>` of :class:`IncorporatedPlace`
        """
        return self._incorporated_places

    @incorporated_places.setter
    def incorporated_places(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def anrc(self):
        """Alaska Native Regional Corporations

        :rtype: :class:`list <python:list>` of :class:`ANRC`
        """
        return self._anrc

    @anrc.setter
    def anrc(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def federal_american_indian_reservations(self):
        """Federal American Indian Reservations

        :rtype: :class:`list <python:list>` of :class:`FederalAmericanIndianReservation`
        """
        return self._federal_american_indian_reservations

    @federal_american_indian_reservations.setter
    def federal_american_indian_reservations(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def off_reservation_trust_lands(self):
        """Off-Reservation Trust Lands

        :rtype: :class:`list <python:list>` of :class:`OffReservationTrustLand`
        """
        return self._off_reservation_trust_lands

    @off_reservation_trust_lands.setter
    def off_reservation_trust_lands(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def state_american_indian_reservations(self):
        """State American Indian Reservation

        :rtype: :class:`list <python:list>` of :class:`StateAmericanIndianReservation`
        """
        return self._state_american_indian_reservations

    @state_american_indian_reservations.setter
    def state_american_indian_reservations(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def hawaiian_home_lands(self):
        """Hawaiian Home Lands

        :rtype: :class:`list <python:list>` of :class:`HawaiianHomeLand`
        """
        return self._hawaiian_home_lands

    @hawaiian_home_lands.setter
    def hawaiian_home_lands(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def anvsa(self):
        """Alaska Native Village Statistical Area

        :rtype: :class:`list <python:list>` of :class:`ANVSA`
        """
        return self._anvsa

    @anvsa.setter
    def anvsa(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def otsa(self):
        """Oklahoma Tribal Statistical Areas

        :rtype: :class:`list <python:list>` of :class:`OTSA`
        """
        return self._otsa

    @otsa.setter
    def otsa(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def sdtsa(self):
        """State Designated Tribal Statistical Areas

        :rtype: :class:`list <python:list>` of :class:`SDTSA`
        """
        return self._sdtsa

    @sdtsa.setter
    def sdtsa(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def tdsa(self):
        """Tribal Designated Statistical Areas

        :rtype: :class:`list <python:list>` of :class:`TDSA`
        """
        return self._tdsa

    @tdsa.setter
    def tdsa(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def american_indian_joint_use_areas(self):
        """American Indian Joint-Use Areas

        :rtype: :class:`list <python:list>` of :class:`AIJUA`
        """
        return self._american_indian_joint_use_areas

    @american_indian_joint_use_areas.setter
    def american_indian_joint_use_areas(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def combined_nectas(self):
        """Combined New England City and Town Areas

        :rtype: :class:`list <python:list>` of :class:`CombinedNECTA`
        """
        return self._combined_nectas

    @combined_nectas.setter
    def combined_nectas(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def necta_divisions(self):
        """New England City and Town Area Divisions

        :rtype: :class:`list <python:list>` of :class:`NECTADivision`
        """
        return self._necta_divisions

    @necta_divisions.setter
    def necta_divisions(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def metrpolitan_nectas(self):
        """Metropolitan New England City and Town Areas

        :rtype: :class:`list <python:list>` of :class:`MetropolitanNECTA`
        """
        return self._metrpolitan_nectas

    @metrpolitan_nectas.setter
    def metrpolitan_nectas(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def micropolitan_nectas(self):
        """Micropolitan New England City and Town Areas

        :rtype: :class:`list <python:list>` of :class:`MicropolitanNECTA`
        """
        return self._micropolitan_nectas

    @micropolitan_nectas.setter
    def micropolitan_nectas(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def urban_growth_areas(self):
        """Urban Growth Areas

        :rtype: :class:`list <python:list>` of :class:`UrbanGrowthArea`
        """
        return self._urban_growth_areas

    @urban_growth_areas.setter
    def urban_growth_areas(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def urbanized_areas(self):
        """Urbanized Areas

        :rtype: :class:`list <python:list>` of :class:`UrbanizedArea`
        """
        return self._urbanized_areas

    @urbanized_areas.setter
    def urbanized_areas(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def urbanized_areas_2010(self):
        """2010 Census Urbanized Areas

        :rtype: :class:`list <python:list>` of :class:`UrbanizedArea_2010`
        """
        return self._urbanized_areas_2010

    @urbanized_areas_2010.setter
    def urbanized_areas_2010(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def urban_clusters(self):
        """Urban Clusters

        :rtype: :class:`list <python:list>` of :class:`UrbanCluster`
        """
        return self._urban_clusters

    @urban_clusters.setter
    def urban_clusters(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def urban_clusters_2010(self):
        """2010 Census Urban Clusters

        :rtype: :class:`list <python:list>` of :class:`urban_clusters_2010`
        """
        return self._urban_clusters_2010

    @urban_clusters_2010.setter
    def urban_clusters_2010(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def traffic_analysis_districts(self):
        """Traffic Analysis Districts

        :rtype: :class:`list <python:list>` of :class:`TrafficAnalysisDistrict`
        """
        return self._traffic_analysis_districts

    @traffic_analysis_districts.setter
    def traffic_analysis_districts(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def traffic_analysis_zones(self):
        """Traffic Analysis Zones

        :rtype: :class:`list <python:list>` of :class:`TrafficAnalysisZone`
        """
        return self._traffic_analysis_zones

    @traffic_analysis_zones.setter
    def traffic_analysis_zones(self, value):
        property_name = currentframe().f_back.f_code.co_name
        self._set_hidden_property(value, property_name)

    @property
    def entity_type(self):
        """The type of geographic entity that the object represents. Supports either:
        ``locations`` or ``geographies``.

        :rtype: :class:`str <python:str>`
        """
        return 'collection'

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
        as_dict = validators.dict(as_dict)
        result = cls()

        for key in GEOGRAPHY_MAP:
            geographies = as_dict.get(key, None)
            if not geographies:
                break

            geography_tuple = GEOGRAPHY_MAP.get(key, None)
            if not geography_tuple:
                continue

            attr_target = geography_tuple[0]
            target_cls = geography_tuple[1]

            setattr(result, attr_target, [target_cls.from_dict(x) for x in geographies])

        return result

    def from_csv_record(cls, csv_record):
        """Create an instance of the geographic entity from its CSV record.

        :param csv_record: The list of columns for the CSV record.
        :type csv_record: :class:`list <python:list>` of :class:`str <python:str>`

        :returns: An instance of the geographic entity.
        :rtype: :class:`GeographicEntity`

        """
        raise TypeError(f'operation not supported on {cls.__name__}')

    def to_dict(self):
        """Returns a :class:`dict <python:dict>` representation of the geographic entity.

        .. note::

          The :class:`dict <python:dict>` representation matches the JSON structure for
          the US Census Geocoder API. This is a not-very-pythonic
          :class:`dict <python:dict>` structure, but at least this ensures idempotency.

        :returns: :class:`dict <python:dict>` representation of the entity.
        :rtype: :class:`dict <python:dict>`
        """
        result = {}
        for key in GEOGRAPHY_MAP:
            geography_tuple = GEOGRAPHY_MAP.get(key)
            attr_target = geography_tuple[0]

            geographies = getattr(self, attr_target)

            if geographies:
                result[key] = [x.to_dict() for x in geographies]

        return result
