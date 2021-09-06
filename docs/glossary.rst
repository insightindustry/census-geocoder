**********
Glossary
**********

.. glossary::

  Benchmark
    The period in time when the geographic data was snapshotted for use / return by the
    `Census Geocoder API`_.

  Census Block
    The single smallest element in the :ref:`core geographic hierarchy <core_geographic_hierarchy>`
    is the **Census Block**. This is the most granular geographical area for which the US
    Census Bureau reports data, and is the smallest geographic unit where data is
    available for 100% of its resident population.

  Census Data
    This is information that is collected from the Constitutionally-mandated decennial
    census, which collects information from 100% of residents in the United States.

  Centroid Latitude
    The latitude coordinate for the geometric center of a
    :term:`geographic area <geography>`.

  Centroid Longitude
    The longitude coordinate for the geometric center of a
    :term:`geographic area <geography>`.

  Internal Point Latitude
    The Census Bureau calculates an internal point (latitude and longitude coordinates)
    for each geographic entity. For many geographic entities, the internal point is at or
    near the geographic center of the entity. For some irregularly shaped entities (such
    as those shaped like a crescent), the calculated geographic center may be located
    outside the boundaries of the entity.  In such instances, the internal point is
    identified as a point inside the entity boundaries nearest to the calculated
    geographic center and, if possible, within a land polygon.

  Internal Point Longitude
    The Census Bureau calculates an internal point (latitude and longitude coordinates)
    for each geographic entity. For many geographic entities, the internal point is at or
    near the geographic center of the entity. For some irregularly shaped entities (such
    as those shaped like a crescent), the calculated geographic center may be located
    outside the boundaries of the entity.  In such instances, the internal point is
    identified as a point inside the entity boundaries nearest to the calculated
    geographic center and, if possible, within a land polygon.

  Forward Geocoding
    Also known as :term:`geocoding`, a process that identifies a specific canonical
    location based on its street address.

  Geocoding
    The act of determining a specific, canonical location based on some input data.

    .. seealso::

      * :term:`Forward Geocoding`
      * :term:`Reverse Geocoding`

  Geography
    A geographical area. Corresponds to a :term:`layer` and represented in the
    **Census Geocoder** as a
    :class:`GeographicArea <census_geocoder.geographies.GeographicArea>`.

  Layer
    When working with the `Census Geocoder API`_ (particularly when
    :ref:`getting geographic area data <geocoding_geographies>`), you have the ability to
    control which *types* of geographic area get returned. These types of geographic area
    are called ":term:`layers <Layer>`". Which layers are available is ultimately
    determined by the :term:`vintage` of the data you are retrieving.

    .. seealso::

      * :doc:`Geographies in the Census Geocoder <geographies>` >
        :ref:`Benchmarks, Vintages, and Layers <benchmarks_vintages_and_layers>`

  One-line Address
    A physical / mailing address represented in a single line of text, like
    ``'4600 Silver Hill Rd, Washington, DC 20233'``.

  Parametrized Address
    An address that has been broken down into its component parts. Thus, a single-line
    address like ``'4600 Silver Hill Rd, Washington, DC 20233'`` gets broken down into:

    * **STREET**: ``'4600 Silver Hill Rd'``
    * **CITY**: ``'Washington'``
    * **STATE**: ``'DC'``
    * **ZIP CODE**: ``'20233'``

  Reverse Geocoding
    A process that identifies a specific canonical location based on its precise
    geographic coordinates (typically expressed as latitude and longitude).

  Sampled Data
    Data reported by the US Census Bureau that is derived from data collected from a
    subset of the resident population (i.e. from a surveyed sample of potential
    respondents).

  Tigerline
    Tigerline and Shapefiles represent the GIS data that defines all of the features
    (places) and geographical areas (polygons) that comprise the mapping data for the
    `Census Geocoder API`_.

  Vintage
    The census or survey data that the geographic area meta-data returned by the
    `Census Geocoder API`_ is linked to, given that geographic area's :term:`benchmark`.

.. _Census Geocoder API: https://geocoding.geo.census.gov/geocoder/
