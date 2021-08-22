**********************************
Using the US Census Geocoder
**********************************

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

.. _introduction:

Introduction
==========================================================

What is Geocoding?
--------------------------

  .. hint::

    The act of determining a specific, canonical location based on some input data.

    .. seealso::

      * :term:`Forward Geocoding`
      * :term:`Reverse Geocoding`

What we typically know about a specific location or geographical area is fuzzy. We might
know part of the address, or refer to the address with abbreviations, or describe a
general area, etc. It's ambiguous, fuzzy, and unclear. That makes getting specific,
canonical, and precise data about that geographic location challenging. Which is where
the process of :term:`geocoding` comes into play.

:term:`Geocoding` is the process of getting a specific, precise, and canonical
determination of a geographical location (a place or geographic feature) or of a
geographical area (encompassing multiple places or geographic features).

A canonical determination of a geographical location or geographical area is defined by
the meta-data that is returned for that location/area. Things like the canonical address,
or various characteristics of the geographical area, etc. represent the "canonical"
information about that location / area.

The process of geocoding returns exactly that kind of canonical / official / unambiguous
meta-data about one or more geographical locations and areas based on a set of inputs.
Some inputs may be expected to be imprecise or partial (e.g. addresses, typically used for
:term:`forward geocoding`) while others are expected to be precise but with incomplete
information (e.g. longitude and latitude coordinates used in :term:`reverse geocoding`).

Why the **Census Geocoder**?
-------------------------------

Geocoding is used for many thing, but the `Census Geocoder API`_ in particular is meant to
provide the US Census Bureau's canonical meta-data about identified locations and areas.
This meta-data is then typically used when executing more in-depth analysis on data
published by the US Census Bureau and other departments of the US federal and state
governments.

Because the US government uses a very complicated and overlapping hierarchy of geographic
areas, it is essential when working with US government data to start from the precise
identification of the geographic areas and locations of interest.

But using the `Census Geocoder API`_ to get this information is non-trivial in its
complexity. That's both because the API has limited documentation on the one hand, and
because its syntax is non-pythonic and requires extensive familiarity with the internals
of the (complicated) datasets that the US Census Bureau manages/publishes.

The **Census Geocoder** library is meant to simplify all of that, by providing an
easy-to-use, batteries-included, pythonic wrapper around the `Census Geocoder API`_.

**Census Geocoder** vs. Alternatives
--------------------------------------------

.. include:: _versus_alternatives.rst

----------------

.. _features:

Census Geocoder Features
============================

* **Easy to adopt**. Just install and import the library, and you can be
  :term:`forward geocoding` and :term:`reverse geocoding` with just two lines of code.
* **Extensive documentation**. One of the main limitations of the Geocoder API is that its
  documentation is scattered across the different datasets released by the Census Bureau,
  making it hard to navigate and understand. We've tried to fix that.
* Location Search

  * Using Geographic Coordinates (reverse geocoding)
  * Using a One-line Address
  * Using a Parametrized Address
  * Using Batched Addresses

* Geography Search

  * Using Geographic Coordinates (reverse geocoding)
  * Using a One-line Address
  * Using a Parametrized Address
  * Using Batched Addresses

* Supports all available :term:`benchmarks <benchmark>`, :term:`vintages <vintage>`, and
  :term:`layers <layer>`.
* Simplified syntax for indicating benchmarks, vintages, and layers.
* No more hard to interpret field names. The library uses simplified (read: human
  understandable) names for location and geography properties.

---------------

.. _overview:

Overview
==================================

How the Census Geocoder Works
----------------------------------

The **Census Geocoder** works with the `Census Geocoder API`_ by providing a thin
Python wrapper around the APIs functionality. Rather than having to construct your own
HTTP requests against the API itself, you can instead work with Python objects and
functions the way you normally would.

In other words, the process is very straightforward:

#. Install the **Census Geocoder** library. (see :ref:`here <installation>`)
#. Import the geocoder. (see :ref:`here <importing>`)
#. Geocode something - either :ref:`locations <geocoding_locations>` or
   :ref:`geographies <geocoding_geographies>`. (see :ref:`here <geocoding>`)
#. Work with your geocoded :ref:`locations <work_with_locations>` or
   :ref:`geographical areas <work_with_geographies>`. (see
   :ref:`here <working_with_results>`)

And that's it! Once you've done the steps above, you can easily geocode one-off requests
or batch many requests into a single transaction.

--------------

.. _installation:

1. Installing the Census Geocoder
=======================================

.. include:: _installation.rst

Dependencies
----------------

.. include:: _dependencies.rst

-------------

.. _importing:

2. Import the Census Geocoder
======================================

.. include:: _import_census_geocoder.rst

---------------

.. _geocoding:

3. Geocoding
===================

Geocoding a location means to retrieve canonical meta-data about that location. Think of
it as getting the "official" details for a given place. Using the **Census Geocoder**, you
can geocode locations given:

  * A single-line address (whole or partial)
  * A :term:`parametrized address` where you know its components parts
  * A set of longitude and latitude coordinates
  * A batch file in CSV or TXT format

However, the `Census Geocoder API`_ provides two different sets of meta-data for any
canonical location:

  * **Location Data**. Think of it as the canonical address for a given location/place.
  * **Geographic Area Data**. Think of it as canonical information about the (different)
    areas that contain the given location/place.

Using the **Census Geocoder** library you can retrieve both types of information.

  .. hint::

    When retrieving geographic area data, you *also* get location data.

.. _geocoding_locations:

Getting Location Data
------------------------

.. include:: _getting_location_data.rst

-----------------

.. _geocoding_geographies:

Getting Geographic Area Data
-----------------------------------

.. include:: _getting_geography_data.rst

.. _using_benchmarks_vintages:

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

+--------------+---------------------+---------------------+---------------------+
|              |                          BENCHMARKS                             |
+              +---------------------+---------------------+---------------------+
|              | Current             | Census2020          | Tab2020             |
+==============+=====================+=====================+=====================+
| **VINTAGES** | Current             | Census2020          | Current             |
+              +---------------------+---------------------+---------------------+
|              | Census2020          | Census2010          | Census2020          |
+              +---------------------+---------------------+---------------------+
|              | ACS2019             |                     | ACS2019             |
+              +---------------------+---------------------+---------------------+
|              | ACS2018             |                     | ACS2018             |
+              +---------------------+---------------------+---------------------+
|              | ACS2017             |                     | ACS2017             |
+              +---------------------+---------------------+---------------------+
|              | Census2010          |                     | Census2010          |
+--------------+---------------------+---------------------+---------------------+

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
      * :meth:`GeographicEntity.from_address() <census_geocoder.geographies.GeographicEntity.from_address>`

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
      * :meth:`GeographicEntity.from_address() <census_geocoder.geographies.GeographicEntity.from_address>`

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
      * :meth:`GeographicEntity.from_coordinates() <census_geocoder.geographies.GeographicEntity.from_coordinates>`

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
      * :meth:`GeographicEntity.from_batch() <census_geocoder.geographies.GeographicEntity.from_batch>`

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
      * :meth:`GeographicEntity.from_address() <census_geocoder.geographies.GeographicEntity.from_address>`

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
      * :meth:`GeographicEntity.from_address() <census_geocoder.geographies.GeographicEntity.from_address>`

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
      * :meth:`GeographicEntity.from_coordinates() <census_geocoder.geographies.GeographicEntity.from_coordinates>`

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
      * :meth:`GeographicEntity.from_batch() <census_geocoder.geographies.GeographicEntity.from_batch>`

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

--------------

.. _working_with_results:

4. Working with Results
=====================================================

.. sidebar:: Locations vs Geographical Areas?

  If all geographical area data is contained within a
  :class:`Location <census_geocoder.locations.Location>`, why differentiate between
  :ref:`working with location data <work_with_locations>` and
  :ref:`working with geographical area data <work_with_geographies>` at all?

  The answer is two-fold: use case and performance. The act of geocoding is very simple
  and occurs at the level of a given
  :class:`Location <census_geocoder.locations.Location>`. This process is done as soon as
  the `Census Geocoder API`_ has determined a canonical location (a
  :class:`MatchedAddress <census_geocoder.locations.MatchedAddress>`). Typically, use
  cases that need that geocoded canonical address require it to be very fast, and that's
  how the `Census Geocoder API`_ has been optimized.

  However, pulling geographical area data *relies* on first determining the canonical
  location. And then, it has to pull a set of additional geographical area meta-data for
  that canonical location's geographical surroundings. That takes time, and the more
  :term:`layers <layer>` you request, the longer that process will take.

  Therefore, both the `Census Geocoder API`_ and the **Census Geocoder** library
  differentiate between the two so that you can use the more-performant location-only
  API calls when appropriate, and the less-performant but more robust geographical area
  API calls as needed.

Now that you've geocoded some data using the **Census Geocoder**, you probably want to
work with your data. Well, that's pretty easy since the **Census Geocoder** returns
native Python objects containing your location or geographical area data.

.. _result_shared_methods:

Shared Methods
-----------------

Most of what you will do with your results is read properties from them so as to consume
or use the canonical location/geographic meta-data in your application. However, there
are a number of methods that are shared between both location data and geographic area
data that may prove helpful:

.. function:: inspect(as_census_fields = False)

  :param as_census_fields: If ``True``, returns the properties using the Census field name
    rather than the **Census Geocoder** (user-friendly) property name. Defaults to
    ``False``.
  :type as_census_fields: :clasS:`bool <python:bool>`

  Returns a list of the properties that are populated with values in the object.

  :rtype: :class:`list <python:list>` of :class:`str <python:str>`

.. function:: to_dict()

  Serializes the data for the location/geographic area into a :class:`dict <python:dict>`
  that conforms directly to the output from the `Census Geocoder API`_.

  :rtype: :class:`dict <python:dict>`

.. function:: to_json()

  Serializes the data for the location/geographic area into a :class:`str <python:str>`
  containing a JSON object that conforms directly to the output from the
  `Census Geocoder API`_.

  :rtype: :class:`str <python:str>`

.. _work_with_locations:

Location Data
------------------

When working with location data, there are two principle sets of meta-data made available:

* **Input**. This is the input that was submitted to the `Census Geocoder API`_, and it
  includes:

  * The address that you submitted.
  * The :term:`benchmark` requested.
  * The :term:`vintage` requested.

* **Matched Addresses**. This is a collection of addresses that the `Census Geocoder API`_
  returned as the canonical addresses for your inputs.

Each matched address exposes its key meta-data, including:

  * The address components in a term:`parametrized <parametrized address>` form.
  * The address in a single-line form.
  * The :term:`Tigerline` identifier information for the address.
  * The side of the street where the address can be found, per the :term:`Tigerline` data.

.. seealso::

  * :class:`Location <census_geocoder.locations.Location>`
  * :class:`MatchedAddress <census_geocoder.locations.MatchedAddress>`

.. _work_with_geographies:

Geographical Area Data
--------------------------

Geographical area data is always returned within the context of a
:class:`MatchedAddress <census_geocoder.locations.MatchedAddress>` instance, which itself
is always contained within a :class:`Location <census_geocoder.locations.Location>`
instance. That matched address will have a ``.geographies`` property, which will contain a
:class:`GeographyCollection <census_geocoder.geographies.GeographyCollection>`. That
``.geographies`` property is what contains the detailed geographical area meta-data for
all geographical areas returned in response to your API request.

Each :term:`layer` requested is contained in a property of the
:class:`GeographyCollection <census_geocoder.geographies.GeographyCollection>`. For
example, the relevant regions would be contained in the ``.regions`` property, while
the relevant census tracts would be contained in the ``.tracts`` property.

.. seealso::

  For a full list of the properties/layers that are available within a
  :class:`GeographyCollection <census_geocoder.geographies.GeographyCollection>`, please
  see the detailed API reference.

  * :class:`GeographyCollection <census_geocoder.geographies.GeographyCollection>`

If a :term:`layer` is not requested (or is irrelevant for a given :term:`benchmark` /
:term:`vintage`), then its corresponding property in the
:class:`GeographyCollection <census_geocoder.geographies.GeographyCollection>` will
be :obj:`None <python:None>`.

Within each layer/property, you will find a collection of
:class:`Geography <census_geocoder.geographies.GeographicArea>` instances (technically,
layer-specific sub-class instances). Each of these instances represents a geographical
area returned by the `Census Geocoder API`_, and their properties will contain the
meta-data returned by that API.

Because different types of geographical area return different meta-data, there is a useful
:meth:`.inspect() <census_geocoder.geographies.GeographicArea.inspect>` method that will tell
you what meta-data properties are available / have data.

The most universal properties (and the ones that are going to prove most useful when
working with other Census Bureau datasets) are:

  * :meth:`.geoid <census_geocoder.geographies.GeographicArea.geoid>` which contains the GEOID
    (unique consolidated identifier for the geographical area)
  * :meth:`.name <census_geocoder.geographies.GeographicArea.name>` which contains the
    human-readable name of the geographical area
  * :meth:`.geography_type <census_geocoder.geographies.GeographicArea.geography_type>` which
    contains a human-readable label for the instances's geographical area/layer type
  * :meth:`.functional_status <census_geocoder.geographies.GeographicArea.functional_status>`
    which contains a human-readable indication of the geographical area's functional status

.. seealso::

  * :class:`GeographyCollection <census_geocoder.geographies.GeographyCollection>`
  * :class:`Geography <census_geocoder.geographies.GeographicArea>`
