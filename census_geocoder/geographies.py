"""
###################################
census_geocoder/geographies.py
###################################

Defines :class:`Geography` geographic entities.

"""
from validator_collection import validators

from census_geocoder import metaclasses
from census_geocoder.constants import FUNCSTAT, LSAD


class Geography(metaclasses.GeographicEntity):
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

        .. info::

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
        self._object_id = validators.string(value, allow_empty = True)

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
        value = validators.string(value, allow_empty = None)
        if value and value.upper() not in FUNCSTAT:
            raise ValueError(f'value ("{value}") not a recognized FUNCSTAT code')

        self._funcstat = value.upper()

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

        self._necta_pci = value.upper()

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

        self._cbsa_pci = value.upper()

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
        self._high_school_grade = validators.string(value, alhigh_empty = True)

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

        .. info::

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


class StateLegislativeDistrictLower(Geography):
    """State Legislative District - Lower"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'State Legislative District - Lower'


class StateLegislativeDistrictUpper(Geography):
    """State Legislative District - Upper"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'State Legislative District - Upper'


class County(Geography):
    """County"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'County'


class ZCTA5(Geography):
    """ZCTA5"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Zip Code Tabulation Area'


class UnifiedSchoolDistrict(Geography):
    """Unified School District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Unified School District'


class VotingDistrict(Geography):
    """Voting District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'County'


class MetropolitanDivision(Geography):
    """Metropolitan Division"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Metropolitan Division'


class State(Geography):
    """State"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'State'


class CensusBlockGroup(Geography):
    """Census Block Group"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Census Block Group'


class CombinedStatisticalArea(Geography):
    """Combined Statistical Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Combined Statistical Area'


class CountySubDivision(Geography):
    """County Sub-division"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'County Sub-division'


class CensusDesignatedPlace(Geography):
    """Census Designated Place"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Census Designated Place'


class CensusDivision(Geography):
    """Census Division"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Division'


class CongressionalDistrict(Geography):
    """Congressional District"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Congressional District'


class CensusRegion(Geography):
    """Census Region"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Region'


class MetropolitanStatisticalArea(Geography):
    """Metropolitan Statistical Area"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Metropolitan Statistical Area'


class CensusBlock(Geography):
    """Census Block"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Census Block'


class CensusTract(Geography):
    """Census Tract"""

    @property
    def geography_type(self):
        """Returns the Geography Type for the given geography."""
        return 'Census Tract'


GEOGRAPHY_MAP = {
    'Census Regions': ('regions', CensusRegion),
    'Census Divisions': ('divisions', CensusDivision),
    'States': ('states', State),
    'Counties': ('counties', County),
    'County Subdivisions': ('county_subdivisions', CountySubDivision),
    'Metropolitan Divisions': ('metropolitan_divisions', MetropolitanDivision),
    'Zip Code Tabulation Areas': ('zcta5', ZCTA5),
    'Unified School Districts': ('unified_school_districts', UnifiedSchoolDistrict),
    'Voting Districts': ('voting_districts', VotingDistrict),
    'State Legislative Districts - Upper': ('state_legislative_districts_upper',
                                            StateLegislativeDistrictUpper),
    'State Legislative Districts - Lower': ('state_legislative_districts_lower',
                                            StateLegislativeDistrictLower),
    '116th Congressional Districts': ('congressional_districts', CongressionalDistrict),
    'Combind Statistical Areas': ('csa', CombinedStatisticalArea),
    'Metropolitan Statistical Areas': ('msa', MetropolitanStatisticalArea),
    'Census Block Groups': ('census_block_groups', CensusBlockGroup),
    'Census Blocks': ('blocks', CensusBlock),
    'Census Tracts': ('tracts', CensusTract),
    'Census Designated Places': ('cdp', CensusDesignatedPlace)
}


class GeographyCollection(metaclasses.BaseEntity):
    """Collection of :class:`Geography` objects."""

    def __init__(self, **kwargs):
        self._regions = []
        self._divisions = []
        self._states = []
        self._counties = []
        self._county_subdivisions = []
        self._metropolitan_divisions = []
        self._zcta5 = []
        self._unified_school_districts = []
        self._voting_districts = []
        self._state_legislative_districts_upper = []
        self._state_legislative_districts_lower = []
        self._congressional_districts = []
        self._csa = []
        self._msa = []
        self._census_block_groups = []
        self._blocks = []
        self._tracts = []
        self._cdp = []

        self = self.from_dict(kwargs)

    @property
    def regions(self):
        """Census Regions

        :rtype: :class:`list <python:list>` of :class:`CensusRegion`
        """
        return self._regions

    @regions.setter
    def regions(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._regions = []
        else:
            self._regions = [x for x in value]

    @property
    def divisions(self):
        """Census Divisions

        :rtype: :class:`list <python:list>` of :class:`CensusDivision`
        """
        return self._divisions

    @divisions.setter
    def divisions(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._divisions = []
        else:
            self._divisions = [x for x in value]

    @property
    def states(self):
        """States

        :rtype: :class:`list <python:list>` of :class:`State`
        """
        return self._states

    @states.setter
    def states(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._states = []
        else:
            self._states = [x for x in value]

    @property
    def counties(self):
        """Census Counties

        :rtype: :class:`list <python:list>` of :class:`County`
        """
        return self._counties

    @counties.setter
    def counties(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._counties = []
        else:
            self._counties = [x for x in value]

    @property
    def county_subdivisions(self):
        """County Sub-division

        :rtype: :class:`list <python:list>` of :class:`CountySubDivision`
        """
        return self._county_subdivisions

    @county_subdivisions.setter
    def county_subdivisions(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._county_subdivisions = []
        else:
            self._county_subdivisions = [x for x in value]

    @property
    def metropolitan_divisions(self):
        """Metropolitan Divisions

        :rtype: :class:`list <python:list>` of :class:`MetropolitanDivision`
        """
        return self._metropolitan_divisions

    @metropolitan_divisions.setter
    def metropolitan_divisions(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._metropolitan_divisions = []
        else:
            self._metropolitan_divisions = [x for x in value]

    @property
    def zcta5(self):
        """Zip Code Tabulation Area

        :rtype: :class:`list <python:list>` of :class:`ZCTA5`
        """
        return self._zcta5

    @zcta5.setter
    def zcta5(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._zcta5 = []
        else:
            self._zcta5 = [x for x in value]

    @property
    def unified_school_districts(self):
        """Unified School Districts

        :rtype: :class:`list <python:list>` of :class:`UnifiedSchoolDistrict`
        """
        return self._unified_school_districts

    @unified_school_districts.setter
    def unified_school_districts(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._unified_school_districts = []
        else:
            self._unified_school_districts = [x for x in value]

    @property
    def voting_districts(self):
        """Voting Districts

        :rtype: :class:`list <python:list>` of :class:`VotingDistrict`
        """
        return self._voting_districts

    @voting_districts.setter
    def voting_districts(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._voting_districts = []
        else:
            self._voting_districts = [x for x in value]

    @property
    def state_legislative_districts_upper(self):
        """State Legislative Districts - Upper

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictUpper`
        """
        return self._state_legislative_districts_upper

    @state_legislative_districts_upper.setter
    def state_legislative_districts_upper(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._state_legislative_districts_upper = []
        else:
            self._state_legislative_districts_upper = [x for x in value]

    @property
    def state_legislative_districts_lower(self):
        """State Legislative Districts - Lower

        :rtype: :class:`list <python:list>` of :class:`StateLegislativeDistrictLower`
        """
        return self._state_legislative_districts_lower

    @state_legislative_districts_lower.setter
    def state_legislative_districts_lower(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._state_legislative_districts_lower = []
        else:
            self._state_legislative_districts_lower = [x for x in value]

    @property
    def congressional_districts(self):
        """Congressional Districts

        :rtype: :class:`list <python:list>` of :class:`CensusDivision`
        """
        return self._congressional_districts

    @congressional_districts.setter
    def congressional_districts(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._congressional_districts = []
        else:
            self._congressional_districts = [x for x in value]

    @property
    def csa(self):
        """Combined Statistical Areas

        :rtype: :class:`list <python:list>` of :class:`CombinedStatisticalArea`
        """
        return self._csa

    @csa.setter
    def csa(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._csa = []
        else:
            self._csa = [x for x in value]

    @property
    def msa(self):
        """Metropolitan Statistical Area

        :rtype: :class:`list <python:list>` of :class:`MetropolitanStatisticalArea`
        """
        return self._msa

    @msa.setter
    def msa(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._msa = []
        else:
            self._msa = [x for x in value]

    @property
    def census_block_groups(self):
        """Census Block Groups

        :rtype: :class:`list <python:list>` of :class:`CensusBlockGroup`
        """
        return self._census_block_groups

    @census_block_groups.setter
    def census_block_groups(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._census_block_groups = []
        else:
            self._census_block_groups = [x for x in value]

    @property
    def blocks(self):
        """Census Blocks

        :rtype: :class:`list <python:list>` of :class:`CensusBlock`
        """
        return self._blocks

    @blocks.setter
    def blocks(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._blocks = []
        else:
            self._blocks = [x for x in value]

    @property
    def tracts(self):
        """Census Tracts

        :rtype: :class:`list <python:list>` of :class:`CensusTract`
        """
        return self._tracts

    @tracts.setter
    def tracts(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._tracts = []
        else:
            self._tracts = [x for x in value]

    @property
    def cdp(self):
        """Census Designated Places

        :rtype: :class:`list <python:list>` of :class:`CensusDesignatedPlace`
        """
        return self._cdp

    @cdp.setter
    def cdp(self, value):
        value = validators.iterable(value, allow_empty = True)
        if not value:
            self._cdp = []
        else:
            self._cdp = [x for x in value]

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

            geography_tuple = GEOGRAPHY_MAP.get(key)
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
