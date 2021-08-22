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

  Forward Geocoding
    Also known as :term:`geocoding`, a process that identifies a specific canonical
    location based on its street address.

  Geocoding
    The act of determining a specific, canonical location based on some input data.

    .. seealso::

      * :term:`Forward Geocoding`
      * :term:`Reverse Geocoding`

  Layer

    .. todo::

      Add this definition

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
