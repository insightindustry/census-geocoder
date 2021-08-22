**********************************
API Reference
**********************************

.. contents::
  :local:
  :depth: 4
  :backlinks: entry

----------

.. module:: census_geocoder.locations

Locations
===============

Location
------------

.. autoclass:: Location
  :members:
  :inherited-members:

--------------

MatchedAddress
------------------

.. autoclass:: MatchedAddress
  :members:
  :inherited-members:

-----------------

.. module:: census_geocoder.geographies

Geographies
=================

GeographyCollection
---------------------

.. autoclass:: GeographyCollection
  :members:
  :inherited-members:

-----------------------

GeographicArea
-------------------

.. autoclass:: GeographicArea
  :members:
  :inherited-members:

--------------------------

Census Block and Related
-----------------------------

.. autoclass:: CensusBlock

.. autoclass:: CensusBlock_2020

------------

Census Block Group
------------------

.. autoclass:: CensusBlockGroup

------------

Tribal Census Block Group
-----------------------------

.. autoclass:: TribalCensusBlockGroup

----------------

Census Tract
-----------------

.. autoclass:: CensusTract

-----------

Tribal Census Tract
---------------------

.. autoclass:: TribalCensusTract

------------------

County and Related
------------------------

.. autoclass:: County

.. autoclass:: CountySubDivision

-----------

State
--------

.. autoclass:: State

----------

PUMA and Related
----------------------

.. autoclass:: PUMA

.. autoclass:: PUMA_2010

----------

State Legislative District and Related
------------------------------------------------

.. autoclass:: StateLegislativeDistrictLower

  .. autoclass:: StateLegislativeDistrictLower_2010

  .. autoclass:: StateLegislativeDistrictLower_2012

  .. autoclass:: StateLegislativeDistrictLower_2016

  .. autoclass:: StateLegislativeDistrictLower_2018

.. autoclass:: StateLegislativeDistrictUpper

  .. autoclass:: StateLegislativeDistrictUpper_2010

  .. autoclass:: StateLegislativeDistrictUpper_2012

  .. autoclass:: StateLegislativeDistrictUpper_2016

  .. autoclass:: StateLegislativeDistrictUpper_2018

--------------

ZCTA5 and Related
---------------------

.. autoclass:: ZCTA5

.. autoclass:: ZCTA_2010

.. autoclass:: ZCTA_2020

-----------

School District-Related
----------------------------

.. autoclass:: UnifiedSchoolDistrict

.. autoclass:: SecondarySchoolDistrict

.. autoclass:: ElementarySchoolDistrict

-------------

Voting District
-----------------

.. autoclass:: VotingDistrict

----------------

Metropolitan Division
------------------------

.. autoclass:: MetropolitanDivision

---------------

Combined Statistical Area
---------------------------

.. autoclass:: CombinedStatisticalArea

-----------------

Tribal Subdivision
---------------------

.. autoclass:: TribalSubDivision

-------------

Census Designated Place
----------------------------

.. autoclass:: CensusDesignatedPlace

---------------

Division
-------------------

.. autoclass:: CensusDivision

------------

Congressional District and Related
-------------------------------------

.. autoclass:: CongressionalDistrict

.. autoclass:: CongressionalDistrict_116

.. autoclass:: CongressionalDistrict_115

.. autoclass:: CongressionalDistrict_113

.. autoclass:: CongressionalDistrict_111

----------

Region
------------------

.. autoclass:: CensusRegion

---------

Metropolitan Statistical Area
--------------------------------

.. autoclass:: MetropolitanStatisticalArea

------------

Micropolitan Statistical Area
-------------------------------

.. autoclass:: MicropolitanStatisticalArea

------------

Estate
-----------

.. autoclass:: Estate

-----------

Subbarrio
------------

.. autoclass:: Subbarrio

------------

Consolidated City
--------------------

.. autoclass:: ConsolidatedCity

----------------

Incorporated Place
----------------------

.. autoclass:: IncorporatedPlace

------------

Alaska Native Regional Corporation
--------------------------------------

.. autoclass:: ANRC

---------

Federal American Indian Reservation
----------------------------------------

.. autoclass:: FederalAmericanIndianReservation

----------

Off-Reservation Trust Land
-----------------------------

.. autoclass:: OffReservationTrustLand

--------

State American Indian Reservation
----------------------------------

.. autoclass:: StateAmericanIndianReservation

--------

Hawaiian Home Land
------------------

.. autoclass:: HawaiianHomeLand

----------

Alaska Native Village Statistical Area
-----------------------------------------

.. autoclass:: ANVSA

--------

Oklahoma Tribal Statistical Areas
-------------------------------------

.. autoclass:: OTSA

---------

State Designated Tribal Statistical Areas
-------------------------------------------

.. autoclass:: SDTSA

------

Tribal Designated Statistical Areas
--------------------------------------

.. autoclass:: TDSA

----------

American Indian Joint-Use Areas
-----------------------------------

.. autoclass:: AIJUA

----------

CombinedNECTA and Related
----------------------------

.. autoclass:: CombinedNECTA

.. autoclass:: NECTADivision

.. autoclass:: MetropolitanNECTA

.. autoclass:: MicropolitanNECTA

--------------

Urban-related Geographical Areas
--------------------------------------

.. autoclass:: UrbanGrowthArea

.. autoclass:: UrbanizedArea

.. autoclass:: UrbanizedArea_2010

.. autoclass:: UrbanCluster

.. autoclass:: UrbanCluster_2010

-----------

Traffic Analysis Zone and Related
-------------------------------------

.. autoclass:: TrafficAnalysisZone

.. autoclass:: TrafficAnalysisDistrict

--------------------------

.. module:: census_geocoder.metaclasses

Census Geocoder Internals
============================

Base Entity
---------------

.. autoclass:: BaseEntity
  :members:
  :inherited-members:

Geographic Entity
--------------------

.. autoclass:: GeographicEntity
  :members:
  :inherited-members:

.. _Census Geocoder API: https://geocoding.geo.census.gov/geocoder/
