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

.. include:: _benchmarks_vintages_layers.rst

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
  see the detailed API reference:

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
