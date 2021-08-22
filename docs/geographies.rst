**************************************
Geographies in the Census Geocoder
**************************************

.. contents::
  :local:
  :depth: 3
  :backlinks: entry

----------

Introduction
===================

We like to think that geography is simple. There's a place, and that place has some
borders, and it's all easy to understand. Intuitive, right?

**Wrong**.

Geography is actually extremely complicated, because it is by its very nature ambiguous.
The only objectively unambiguous definition of a geographic area is a pair of
longitude/latitude coordinates. When you start considering ways in which geographic areas
overlap or roll into a hierarchy, it gets even more complicated because then you need to
consider how each geographic area gets defined and overlaps.

Then, when you consider how such geographic hierarchies map to data (which itself
represents a point-in-time), it gets even more complicated. That's because geographic
definitions change all the time. Street names change, town names change, borders shift,
etc.

And the `Census Geocoder API`_ and the US Census Bureau data that it corresponds to has to
inherently account for all of these complexities. Which makes the way the
`Census Geocoder API`_ handles geographic areas complicated.

-------------

.. _benchmarks_vintages_and_layers:

Benchmarks, Vintages, and Layers
=====================================

.. include:: _benchmarks_vintages_layers.rst

-------------

.. _census_geographic_hierarchies:

Census Geographic Hierarchies Explained
==========================================

As you can tell from the list of layers above, there are lots of different types of
geographic areas supported by the `Census Geocoder API`_. These areas overlap in lots of
different ways, and the US Census Bureau's documentation explaining this can be a little
hard to find. Therefore, I've tried to explain the hierarchies' logic in straightforward
language and diagrams below.

.. seealso::

  * :download:`U.S. Census Bureau Geographic Entities and Concepts (PDF) </_static/geoareaconcepts.pdf>`
  * :download:`The Standard Hierarchy of Census Geographic Entities (PDF) </_static/geodiagram.pdf>`
  * :download:`Hierarchy of American Indian, Alaska Native, and Native Hawaiian Areas (PDF) </_static/aianhh_diag.pdf>`
  * :download:`The Standard Hierarchy of Census Geographic Entities in Island Areas (PDF) </_static/geodiagram_islandareas.pdf>`

.. _core_geographic_hierarchy:

Core Hierarchy
----------------------

.. figure:: /_static/core_hierarchy.jpg
  :alt: Core Geographic Hierarchy
  :align: center

We should start by understanding the "core" of the US Census Bureau's hierarchy, and
working our way "up" from the smallest section. This core hierarchy by definition does
not overlap. Each area within a particular level of the hierarchy is precisely defined,
with those definitions represented in the :term:`Tigerline / Shapefile <Tigerline>` data
published by the US Census Bureau.

.. data:: Census Block

  The single smallest element in the core hierarchy is the **Census Block**. This is the
  most granular geographical area for which the US Census Bureau reports data, and is
  the smallest geographic unit where data is available for 100% of its resident
  population.

.. data:: Block Groups

  Collections of **Census Blocks**. In general, the population size for block groups are
  600 - 3,000.

  This is the most granular geographical area for which the US Census Bureau reports
  :term:`sampled data`.

.. data:: Census Tracts

  Collections of **Block Groups**. They are considered small, permanent, and consistent
  statistical sections of their containing county.

  Optimally contains 4,000 people, and range from 1,200 - 8,000 people.

.. data:: Counties and County Equivalents

  The first administrative (government administered) area defined in the core
  hierarchy. Counties have their own administrations, subordinate to the state
  administration. Defined as a collection of **Census Tracts**.

  .. note::

    In 48 states, "counties" in the data correspond to "counties" in the their legal
    administration.

    In MD, MO, NV, and VA, Independent Cities are treated as counties.

    In LA, parishes are treated as counties.

    In Alaska, Cities, Boroughs, Municipalities, and Census Areas are treated as counties.

    In Puerto Rico, municipios are treated as counties.

    In American Samoa, islands and districts are treated as counties.

    In the Northern Marianas, municipalities are treated as counties.

    In the Virgin Islands, islands are treated as counties.

    Guam and the District of Columbia are each treated as a county.

  In addition to breaking down into census tracts, counties may also be broken down into:

  * County Subdivisions
  * Voting Districts

.. data:: States

  The federally-constituted state (or territory, as applicable). Defined as a collection
  of **Counties**.

  In addition to breaking down into counties, states may also be broken down into:

  * School Districts
  * Congressional Districts
  * State Legislative Districts

  States also include **Places**, which are named entities in several types:

    * **Incorporated Places**. Which are legally-bounded entities with some form of local
      governance recognized by the state. Typically they are referred to as cities,
      boroughs, towns, or villages.
    * **Census Designated Places**. Which are statistical agglomerations of unincorporated
      areas that are still identifiable by name.
    * **Consolidated Cities**. Which are statistical agglomerations of
      city-related places.

.. data:: Divisions

  Collections of states that comprise a division within the USGIS definition
  of divisions.

.. data:: Regions

  Collection of divisions that comprise a region, per the USGIS
  definition.

.. data:: National

  Collection of all regions, that in total makes up the United States of America.

  In addition to breaking down into regions, the country can also be broken down into:

  * Zip Code Tabulation Areas

  .. hint::

    It may be surprising that zip code tabulation areas are not defined at the state
    level. There are several important reasons for this fact:

    * First, ZCTAs in the Census definition are only *approximate* matches for the US
      Postal Service's zip code definitions. They are *statistical* entities that are
      composed of Census Blocks, and so may not align perfectly to building zip codes.
    * Zip codes in general are federally administered by the US Postal Service, and
      in some (very rare!) cases zip codes may actually straddle state lines.

  The country also contains a number of standalone geographical areas, which while not
  comprising 100% of the nation, may represent significant sections of the country or
  its component parts. In particular, the country also includes:

  * **Core-based Statistical Areas**. These are statistical areas that are composed of
    census blocks and which are used to represent different population agglomerations.
    Examples include Metropolitan Statistical Areas (which are statistical agglomerations
    for a given metro area), or NECTAs (New England City and Town Areas, which are
    division-specific agglomerations of New England communities).
  * **Urban Areas**. These are statistical areas that are composed of census blocks, and
    which have two types: urban clusters (which contain 2,500 - 50,000 people) and
    urbanized areas (which contain 50,000 or more people).


Secondary Hierarchies
--------------------------

Budding off from the :ref:`core hierarchy <core_geographic_hierarchy>`, specific
geographic entities can either be broken down or contain other secondary hierarchies.
Most secondary hierarchies are flat (i.e. they are themselves defined by a collection of
:term:`census blocks <census block>`), but they may be composed of different *types* of
entities.

A good example of this pattern is the secondary-hierarchy concept of "School District".
While school districts cannot be broken down further (they are defined by census blocks),
there are three types of school district that are available within the US Census data:
**Unified School Districts**, **Secondary School Districts**, and
**Elementary School Districts**.

Places
^^^^^^^^^^

Another major secondary hierarchy with similar "type-based" differentiation is the concept
of "places". There are multiple types of place, including **Census Designated Places**,
**Incorporated Places**, and **Consolidated Cities**. These are conceptual areas, which in
turn can all be broken down into their component census blocks.

The most important types of places are:

  * **Incorporated Places**. Which are legally-bounded entities with some form of local
    governance recognized by the state. Typically they are referred to as cities,
    boroughs, towns, or villages.
  * **Census Designated Places**. Which are statistical agglomerations of unincorporated
    areas that are still identifiable by name.

AIANHH Hierarchy
--------------------

Besides the :ref:`core hierarchy <core_geographic_hierarchy>` described above, the US
Census Bureau also reports data within an American Indian, Alaska Native, and Native
Hawaiaan-oriented hierarchy.

This hierarchy is also built by rolling-up :term:`Census Blocks <Census Block>`, however
it does not conform to either the state or county-level definitions used in the core
hierarchy. This is because tribal population groups, federally-designated American Indian
areas, tribal-designated areas, etc. may often cross state, division, or regional lines.

.. figure:: /_static/aianhh_diag.png
  :alt: American Indian, Alaska Native, and Native Hawaiian Hierarchy
  :align: center
