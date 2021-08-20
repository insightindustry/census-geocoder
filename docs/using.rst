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

.. _geocode_locations:

3a. Geocode Locations
=========================

.. todo::

  Add a section with tabs for each method to geocode locations.

-----------------

.. _geocode_geographies:

3b. Geocode Geographies
==============================================

.. todo::

  Add a section with tabs for each method to geocode locations.

--------------

.. _work_with_results:

4. Work with Results
=====================================================

Location Data
------------------

.. todo::

  Add section

Geography Data
-------------------

.. todo::

  Add section
