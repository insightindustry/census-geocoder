Benchmarks and Vintages
-----------------------------

The data returned by the `Census Geocoder API`_ is different from typical geocoding
services, in that it is time-sensitive. A geocoding service like the Google Maps API or
Here.com only cares about the *current* location. But the US Census Bureau's information
is inherently linked to the statistical data collected by the US Census Bureau at
particular moments in time.

Thus, when making requests against the `Census Geocoder API`_ you are always asking for
geographic location data or geographic area data as of a particular date. You might think
"geographies don't change", but in actuality they are constantly evolving. Congressional
districts, school districts, town lines, county lines, street names, house numbers, etc.
are all constantly evolving. And to ensure that the statistical data is tied to the
locations properly, that alignment needs to be maintained through two key concepts:

  * :term:`Benchmarks <benchmark>`
  * :term:`Vintages <vintage>`

The :term:`benchmark` is the time period when geographic information was snapshotted for
use / publication in the `Census Geocoder API`_. This is typically done twice per year,
and represents the "geographic definitions as of the time period indicated by the
benchmark".

The :term:`vintage` is the census or survey data that the geographies are linked to. Thus,
the geographic identifiers or statistical data associated with locations or geographic
areas within a given benchmark are *also* linked to a particular vintage of census/survey
data. Trying to use those identifiers or statistical data with a different vintage of data
may produce inaccurate results.

The `Census Geocoder API`_ supports a variety of benchmarks and vintages, and they are
unfortunately poorly documented and difficult to interpret. Therefore, the
**Census Geocoder** has been designed to streamline and simplify their usage.

Vintages are only available for a given benchmark. The table below provides guidance on
the vintages and benchmarks supported by the **Census Geocoder**:

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


When using the **Census Geocoder**, you can supply the :term:`benchmark` and
:term:`vintage` directly when executing your geocoding request:

.. tabs::

  .. tab:: Single-line Address

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_address('4600 Silver Hill Rd, Washington, DC 20233',
                                              benchmark = 'Current',
                                              vintage = 'ACS2019')

      result = geocoder.geography.from_address('4600 Silver Hill Rd, Washington, DC 20233',
                                               benchmark = 'Current',
                                               vintage = 'ACS2019')

    .. seealso::

      * :meth:`Location.from_address() <census_geocoder.locations.Location.from_address>`
      * :meth:`GeographicArea.from_address() <census_geocoder.geographies.GeographicArea.from_address>`

  .. tab:: Parametrized Address

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_address(street = '4600 Silver Hill Rd',
                                              city = 'Washington',
                                              state = 'DC',
                                              zip_code = '20233',
                                              benchmark = 'Current',
                                              vintage = 'ACS2019')

      result = geocoder.geography.from_address(street = '4600 Silver Hill Rd',
                                               city = 'Washington',
                                               state = 'DC',
                                               zip_code = '20233',
                                               benchmark = 'Current',
                                               vintage = 'ACS2019')

    .. seealso::

      * :meth:`Location.from_address() <census_geocoder.locations.Location.from_address>`
      * :meth:`GeographicArea.from_address() <census_geocoder.geographies.GeographicArea.from_address>`

  .. tab:: Coordinates

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_coordinates(longitude = -76.92744,
                                                  latitude = 38.845985,
                                                  benchmark = 'Current',
                                                  vintage = 'ACS2019')

      result = geocoder.geography.from_coordinates(longitude = -76.92744,
                                                   latitude = 38.845985,
                                                   benchmark = 'Current',
                                                   vintage = 'ACS2019')

    .. seealso::

      * :meth:`Location.from_coordinates() <census_geocoder.locations.Location.from_coordinates>`
      * :meth:`GeographicArea.from_coordinates() <census_geocoder.geographies.GeographicArea.from_coordinates>`

  .. tab:: Batch File

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_batch(file_ = '/my-csv-file.csv',
                                            benchmark = 'Current',
                                            vintage = 'ACS2019')

      result = geocoder.geography.from_batch(file_ = '/my-csv-file.csv',
                                             benchmark = 'Current',
                                             vintage = 'ACS2019')

    .. seealso::

      * :meth:`Location.from_batch() <census_geocoder.locations.Location.from_batch>`
      * :meth:`GeographicArea.from_batch() <census_geocoder.geographies.GeographicArea.from_batch>`

.. hint::

  Several important things to be aware of when it comes to benchmarks and vintages in the
  **Census Geocoder** library:

  Unless over-ridden by the ``CENSUS_GEOCODER_BENCHMARK`` or ``CENSUS_GEOCODER_VINTAGE``
  environment variables, the benchmark and vintage default to ``'Current'`` and
  ``'Current'`` respectively.

  The benchmark and vintage are case-insensitive. This means that you can supply
  ``'Current'``, ``'CURRENT'``, or ``'current'`` and it will all work the same.

  If you want to set a different default benchmark or vintage, you can do so by setting
  ``CENSUS_GEOCODER_BENCHMARK`` and ``CENSUS_GEOCODER_VINTAGE`` environment variables
  to the defaults you want to use.

Layers
--------------

When working with the `Census Geocoder API`_ (particularly when
:ref:`getting geographic area data <geocoding_geographies>`), you have the ability to
control which *types* of geographic area get returned. These types of geographic area
are called ":term:`layers <Layer>`".

An example of two different "layers" might be "State" and "County". These are two
different types of geographic area, one of which (County) may be encompassed by the other
(State). In general, geographic areas within the same layer cannot and do not overlap.
However different layers can and *do* overlap, where one layer (State) may contain
multiple other layers (Counties), or one layer (Metropolitan Statistical Areas) may
partially overlap multiple entities within a different layer (States).

When using the **Census Geocoder** you can easily specify the layers of data that you
want returned. Unless overridden by the ``CENSUS_GEOCODER_LAYERS`` environment variable,
the layers returned will always default to ``'all'``.

Which layers are available is ultimately determined by the :term:`vintage` of the data you
are retrieving. The following represents the list of layers available in each vintage:

.. panels::

  .. dropdown:: Current

    * 2010 Census Public Use Microdata Areas
    * 2010 Census PUMAs
    * 2010 PUMAs
    * Census Public Use Microdata Areas
    * Census PUMAs
    * PUMAs
    * 2020 Census ZIP Code Tabulation Areas
    * 2020 Census ZCTAs
    * Census ZCTAs
    * ZCTAs
    * Tribal Census Tracts
    * Tribal Block Groups
    * Census Tracts
    * Census Block Groups
    * 2020 Census Blocks
    * Census Blocks
    * Blocks
    * Unified School Districts
    * Secondary School Districts
    * Elementary School Districts
    * Estates
    * County Subdivisions
    * Subbarrios
    * Consolidated Cities
    * Incorporated Places
    * Census Designated Places
    * CDPs
    * Alaska Native Regional Corporations
    * Tribal Subdivisions
    * Federal American Indian Reservations
    * Off-Reservation Trust Lands
    * State American Indian Reservations
    * Hawaiian Home Lands
    * Alaska Native Village Statistical Areas
    * Oklahoma Tribal Statistical Areas
    * State Designated Tribal Stastical Areas
    * Tribal Designated Statistical Areas
    * American Indian Joint-Use Areas
    * 116th Congressional Districts
    * Congressional Districts
    * 2018 State Legislative Districts - Upper
    * State Legislative Districts - Upper
    * 2018 State Legislative Districts - Lower
    * State Legislative Districts - Lower
    * Census Divisions
    * Divisions
    * Census Regions
    * Regions
    * Combined New England City and Town Areas
    * Combined NECTAs
    * New England City and Town Area Divisions
    * NECTA Divisions
    * Metropolitan New England City and Town Areas
    * Metropolitan NECTAs
    * Micropolitan New England City and Town Areas
    * Micropolitan NECTAs
    * Combined Statistical Areas
    * CSAs
    * Metropolitan Divisions
    * Metropolitan Statistical Areas
    * Micropolitan Statistical Areas
    * States
    * Counties

  ---

  .. dropdown:: Census2020

    * Urban Growth Areas
    * Tribal Census Tracts
    * Tribal Block Groups
    * Census Tracts
    * Census Block Groups
    * Block Groups
    * Census Blocks
    * Blocks
    * Unified School Districts
    * Secondary School Districts
    * Elementary School Districts
    * Estates
    * County Subdivisions
    * Subbarrios
    * Consolidated Cities
    * Incorporated Places
    * Census Designated Places
    * CDPs
    * Alaska Native Regional Corporations
    * Tribal Subdivisions
    * Federal American Indian Reservations
    * Off-Reservation Trust Lands
    * State American Indian Reservations
    * Hawaiian Home Lands
    * Alaska Native Village Statistical Areas
    * Oklahoma Tribal Statistical Areas
    * State Designated Tribal Stastical Areas
    * Tribal Designated Statistical Areas
    * American Indian Joint-Use Areas
    * 116th Congressional Districts
    * Congressional Districts
    * 2018 State Legislative Districts - Upper
    * State Legislative Districts - Upper
    * 2018 State Legislative Districts - Lower
    * State Legislative Districts - Lower
    * Voting Districts
    * Census Divisions
    * Divisions
    * Census Regions
    * Regions
    * Combined New England City and Town Areas
    * Combined NECTAs
    * New England City and Town Area Divisions
    * NECTA Divisions
    * Metropolitan New England City and Town Areas
    * Metropolitan NECTAs
    * Micropolitan New England City and Town Areas
    * Micropolitan NECTAs
    * Combined Statistical Areas
    * CSAs
    * Metropolitan Divisions
    * Metropolitan Statistical Areas
    * Micropolitan Statistical Areas
    * States
    * Counties
    * Zip Code Tabulation Areas
    * ZCTAs

  ---

  .. dropdown:: ACS2019

    * 2010 Census Public Use Microdata Areas
    * 2010 Census PUMAs
    * 2010 PUMAs
    * Census Public Use Microdata Areas
    * Census PUMAs
    * PUMAs
    * 2010 Census ZIP Code Tabulation Areas
    * 2010 Census ZCTAs
    * Census ZCTAs
    * ZCTAs
    * Tribal Census Tracts
    * Tribal Block Groups
    * Census Tracts
    * Census Block Groups
    * Unified School Districts
    * Secondary School Districts
    * Elementary School Districts
    * Estates
    * County Subdivisions
    * Subbarrios
    * Consolidated Cities
    * Incorporated Places
    * Census Designated Places
    * CDPs
    * Alaska Native Regional Corporations
    * Tribal Subdivisions
    * Federal American Indian Reservations
    * Off-Reservation Trust Lands
    * State American Indian Reservations
    * Hawaiian Home Lands
    * Alaska Native Village Statistical Areas
    * Oklahoma Tribal Statistical Areas
    * State Designated Tribal Stastical Areas
    * Tribal Designated Statistical Areas
    * American Indian Joint-Use Areas
    * 116th Congressional Districts
    * Congressional Districts
    * 2018 State Legislative Districts - Upper
    * State Legislative Districts - Upper
    * 2018 State Legislative Districts - Lower
    * State Legislative Districts - Lower
    * Census Divisions
    * Divisions
    * Census Regions
    * Regions
    * 2010 Census Urbanized Areas
    * Census Urbanized Areas
    * Urbanized Areas
    * 2010 Census Urban Clusters
    * Census Urban Clusters
    * Urban Clusters
    * Combined New England City and Town Areas
    * Combined NECTAs
    * New England City and Town Area Divisions
    * NECTA Divisions
    * Metropolitan New England City and Town Areas
    * Metropolitan NECTAs
    * Micropolitan New England City and Town Areas
    * Micropolitan NECTAs
    * Combined Statistical Areas
    * CSAs
    * Metropolitan Divisions
    * Metropolitan Statistical Areas
    * Micropolitan Statistical Areas
    * States
    * Counties

  ---

  .. dropdown:: ACS2018

    * 2010 Census Public Use Microdata Areas
    * 2010 Census PUMAs
    * 2010 PUMAs
    * Census Public Use Microdata Areas
    * Census PUMAs
    * PUMAs
    * 2010 Census ZIP Code Tabulation Areas
    * 2010 Census ZCTAs
    * Census ZCTAs
    * ZCTAs
    * Tribal Census Tracts
    * Tribal Block Groups
    * Census Tracts
    * Census Block Groups
    * Unified School Districts
    * Secondary School Districts
    * Elementary School Districts
    * Estates
    * County Subdivisions
    * Subbarrios
    * Consolidated Cities
    * Incorporated Places
    * Census Designated Places
    * CDPs
    * Alaska Native Regional Corporations
    * Tribal Subdivisions
    * Federal American Indian Reservations
    * Off-Reservation Trust Lands
    * State American Indian Reservations
    * Hawaiian Home Lands
    * Alaska Native Village Statistical Areas
    * Oklahoma Tribal Statistical Areas
    * State Designated Tribal Stastical Areas
    * Tribal Designated Statistical Areas
    * American Indian Joint-Use Areas
    * 116th Congressional Districts
    * Congressional Districts
    * 2018 State Legislative Districts - Upper
    * State Legislative Districts - Upper
    * 2018 State Legislative Districts - Lower
    * State Legislative Districts - Lower
    * Census Divisions
    * Divisions
    * Census Regions
    * Regions
    * 2010 Census Urbanized Areas
    * Census Urbanized Areas
    * Urbanized Areas
    * 2010 Census Urban Clusters
    * Census Urban Clusters
    * Urban Clusters
    * Combined New England City and Town Areas
    * Combined NECTAs
    * New England City and Town Area Divisions
    * NECTA Divisions
    * Metropolitan New England City and Town Areas
    * Metropolitan NECTAs
    * Micropolitan New England City and Town Areas
    * Micropolitan NECTAs
    * Combined Statistical Areas
    * CSAs
    * Metropolitan Divisions
    * Metropolitan Statistical Areas
    * Micropolitan Statistical Areas
    * States
    * Counties

  ---

  .. dropdown:: ACS2017

    * 2010 Census Public Use Microdata Areas
    * 2010 Census PUMAs
    * 2010 PUMAs
    * Census Public Use Microdata Areas
    * Census PUMAs
    * PUMAs
    * 2010 Census ZIP Code Tabulation Areas
    * 2010 Census ZCTAs
    * Census ZCTAs
    * ZCTAs
    * Tribal Census Tracts
    * Tribal Block Groups
    * Census Tracts
    * Census Block Groups
    * Unified School Districts
    * Secondary School Districts
    * Elementary School Districts
    * Estates
    * County Subdivisions
    * Subbarrios
    * Consolidated Cities
    * Incorporated Places
    * Census Designated Places
    * CDPs
    * Alaska Native Regional Corporations
    * Tribal Subdivisions
    * Federal American Indian Reservations
    * Off-Reservation Trust Lands
    * State American Indian Reservations
    * Hawaiian Home Lands
    * Alaska Native Village Statistical Areas
    * Oklahoma Tribal Statistical Areas
    * State Designated Tribal Stastical Areas
    * Tribal Designated Statistical Areas
    * American Indian Joint-Use Areas
    * 115th Congressional Districts
    * Congressional Districts
    * 2016 State Legislative Districts - Upper
    * State Legislative Districts - Upper
    * 2016 State Legislative Districts - Lower
    * State Legislative Districts - Lower
    * Census Divisions
    * Divisions
    * Census Regions
    * Regions
    * 2010 Census Urbanized Areas
    * Census Urbanized Areas
    * Urbanized Areas
    * 2010 Census Urban Clusters
    * Census Urban Clusters
    * Urban Clusters
    * Combined New England City and Town Areas
    * Combined NECTAs
    * New England City and Town Area Divisions
    * NECTA Divisions
    * Metropolitan New England City and Town Areas
    * Metropolitan NECTAs
    * Micropolitan New England City and Town Areas
    * Micropolitan NECTAs
    * Combined Statistical Areas
    * CSAs
    * Metropolitan Divisions
    * Metropolitan Statistical Areas
    * Micropolitan Statistical Areas
    * States
    * Counties

  ---

  .. dropdown:: Census2010

    * Public Use Microdata Areas
    * PUMAs
    * Traffic Analysis Districts
    * TADs
    * Traffic Analysis Zones
    * TAZs
    * Urban Growth Areas
    * ZIP Code Tabulation Areas
    * Zip Code Tabulation Areas
    * ZCTAs
    * Tribal Census Tracts
    * Tribal Block Groups
    * Census Tracts
    * Census Block Groups
    * Census Blocks
    * Blocks
    * Unified School Districts
    * Secondary School Districts
    * Elementary School Districts
    * Estates
    * County Subdivisions
    * Subbarrios
    * Consolidated Cities
    * Incorporated Places
    * Census Designated Places
    * CDPs
    * Alaska Native Regional Corporations
    * Tribal Subdivisions
    * Federal American Indian Reservations
    * Off-Reservation Trust Lands
    * State American Indian Reservations
    * Hawaiian Home Lands
    * Alaska Native Village Statistical Areas
    * Oklahoma Tribal Statistical Areas
    * State Designated Tribal Stastical Areas
    * Tribal Designated Statistical Areas
    * American Indian Joint-Use Areas
    * 113th Congressional Districts
    * 111th Congressional Districts
    * 2012 State Legislative Districts - Upper
    * 2012 State Legislative Districts - Lower
    * 2010 State Legislative Districts - Upper
    * 2010 State Legislative Districts - Lower
    * Voting Districts
    * Census Divisions
    * Divisions
    * Census Regions
    * Regions
    * Urbanized Areas
    * Urban Clusters
    * Combined New England City and Town Areas
    * Combined NECTAs
    * New England City and Town Area Divisions
    * NECTA Divisions
    * Metropolitan New England City and Town Areas
    * Metropolitan NECTAs
    * Micropolitan New England City and Town Areas
    * Micropolitan NECTAs
    * Combined Statistical Areas
    * CSAs
    * Metropolitan Divisions
    * Metropolitan Statistical Areas
    * Micropolitan Statistical Areas
    * States
    * Counties

.. note::

  You may notice that there are (logical) duplicate layers in the lists above, for example
  "2010 Census PUMAs" and "2010 Census Public Use Microdata Areas". This is because there
  are multiple ways that users of Census data may refer to particular layers in their
  work. This duplication is purely for the convenience of **Census Geocoder** users, since
  the `Census Geocoder API`_ actually uses numerical identifiers for the layers returned.

When geocoding data, you can simply supply the layers you want using the ``layers``
keyword argument as below:

.. tabs::

  .. tab:: Single-line Address

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_address('4600 Silver Hill Rd, Washington, DC 20233',
                                              benchmark = 'Current',
                                              vintage = 'ACS2019',
                                              layers = 'Census Tracts, States, CDPs, Divisions')

      result = geocoder.geography.from_address('4600 Silver Hill Rd, Washington, DC 20233',
                                               benchmark = 'Current',
                                               vintage = 'ACS2019',
                                               layers = 'Census Tracts, States, CDPs, Divisions')

    .. seealso::

      * :meth:`Location.from_address() <census_geocoder.locations.Location.from_address>`
      * :meth:`GeographicArea.from_address() <census_geocoder.geographies.GeographicArea.from_address>`

  .. tab:: Parametrized Address

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_address(street = '4600 Silver Hill Rd',
                                              city = 'Washington',
                                              state = 'DC',
                                              zip_code = '20233',
                                              benchmark = 'Current',
                                              vintage = 'ACS2019',
                                              layers = 'Census Tracts, States, CDPs, Divisions')

      result = geocoder.geography.from_address(street = '4600 Silver Hill Rd',
                                               city = 'Washington',
                                               state = 'DC',
                                               zip_code = '20233',
                                               benchmark = 'Current',
                                               vintage = 'ACS2019',
                                               layers = 'Census Tracts, States, CDPs, Divisions')

    .. seealso::

      * :meth:`Location.from_address() <census_geocoder.locations.Location.from_address>`
      * :meth:`GeographicArea.from_address() <census_geocoder.geographies.GeographicArea.from_address>`

  .. tab:: Coordinates

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_coordinates(longitude = -76.92744,
                                                  latitude = 38.845985,
                                                  benchmark = 'Current',
                                                  vintage = 'ACS2019',
                                                  layers = 'Census Tracts, States, CDPs, Divisions')

      result = geocoder.geography.from_coordinates(longitude = -76.92744,
                                                   latitude = 38.845985,
                                                   benchmark = 'Current',
                                                   vintage = 'ACS2019',
                                                   layers = 'Census Tracts, States, CDPs, Divisions')

    .. seealso::

      * :meth:`Location.from_coordinates() <census_geocoder.locations.Location.from_coordinates>`
      * :meth:`GeographicArea.from_coordinates() <census_geocoder.geographies.GeographicArea.from_coordinates>`

  .. tab:: Batch File

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_batch(file_ = '/my-csv-file.csv',
                                            benchmark = 'Current',
                                            vintage = 'ACS2019')

      result = geocoder.geography.from_batch(file_ = '/my-csv-file.csv',
                                             benchmark = 'Current',
                                             vintage = 'ACS2019',
                                             layers = 'Census Tracts, States, CDPs, Divisions')

    .. seealso::

      * :meth:`Location.from_batch() <census_geocoder.locations.Location.from_batch>`
      * :meth:`GeographicArea.from_batch() <census_geocoder.geographies.GeographicArea.from_batch>`

.. hint::

  When using the **Census Geocoder** to return geographic area data, you can request
  multiple layers worth of data by passing them in a comma-delimited string. This will
  return separate data for each layer indicated. The comma-delimited string can include
  white-space for easy readability, which means that the following two values are
  considered identical:

    * ``layers = 'Census Tracts, States, CDPs, Divisions'``
    * ``layers = 'Census Tracts,States,CDPs,Divisions'``

  To retrieve all available layers that have data for a given location, you can submit
  ``'all'``. Unless you have set the ``CENSUS_GEOCODER_LAYERS`` environment variable to a
  different value, ``'all'`` is the default set of layers that will be returned.

  Note that layer names in the **Census Geocoder** are case-insensitive.
