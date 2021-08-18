####################################################
US Census Geocoder
####################################################

**(Unofficial) Python Binding for the US Census Geocoder API**

The **US Census Geocoder** is a Python library that provides Python bindings for the
`U.S. Census Geocoder API <https://geocoding.geo.census.gov/geocoder/>`_. It enables
you to use simple Python function calls to retrieve Python object representations of
geographic meta-data for the addresses or coordinates that you are searching for.

.. warning::

  The **US Census Geocoder** is completely unofficial, and is in no way affiliated with
  the US Government or the US Census Bureau. We strongly recommend that you do business
  with them directly as needed, and simply provide this Python library as a facilitator
  for your programmatic interactions with the excellent services provided by the US Census
  Bureau.

**COMPLETE DOCUMENTATION:** https://census_geocoder.readthedocs.org/en/latest.html

.. contents::
 :depth: 3
 :backlinks: entry

-----------------

***************
Installation
***************

To install the **US Census Geocoder**, just execute:

.. code:: bash

 $ pip install census-geocoder


Dependencies
==============

.. list-table::
   :widths: 100
   :header-rows: 1

   * - Python 3.x
   * - | * `Validator-Collection v1.5 <https://github.com/insightindustry/validator-collection>`_ or higher
       | * `Backoff-Utils v.1.0 <https://github.com/insightindustry/backoff-utils>`_ or higher

-------------

**************************************
Key US Census Geocoder Features
**************************************

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

* Supports all available benchmarks and vintages

------------------

*********************************
Hello World and Basic Usage
*********************************

1. Import the Census Geocoder
================================

.. code-block:: python

  from census_geocoder import geocoder

2. Execute a Coding Request
===================================

Using a One-line Address
----------------------------

.. code-block:: python

  location = geocoder.location.from_address('4600 Silver Hill Rd, Washington, DC 20233')

  geography = geocoder.geography.from_address('4600 Silver Hill Rd, Washington, DC 20233')


Using a Parametrized Address
--------------------------------

.. code-block:: python

  location = geocoder.location.from_address(street_1 = '4600 Silver Hill Rd',
                                            city = 'Washington',
                                            state = 'DC',
                                            zip_code = '20233')

  geography = geocoder.geography.from_address(street_1 = '4600 Silver Hill Rd',
                                              city = 'Washington',
                                              state = 'DC',
                                              zip_code = '20233')


Using Batched Addresses
---------------------------

.. code-block:: python

  # Via a CSV File
  location = geocoder.location.from_batch('my-batched-address-file.csv')

  geography = geocoder.geography.from_batch('my-batched-address-file.csv')

  # Via a list of Addresses
  location = geocoder.location.from_batch(['4600 Silver Hill Rd, Washington, DC 20233',
                                           '1600 Pennsylvania Ave NW, Washington, DC 20500'])

  geography = geocoder.geography.from_batch(['4600 Silver Hill Rd, Washington, DC 20233',
                                             '1600 Pennsylvania Ave NW, Washington, DC 20500'])


Using Coordinates
-------------------------

.. code-block:: python

  location = geocoder.location.from_coordinates(latitude = 38.845985,
                                                longitude = -76.92744)


  geography = geocoder.geography.from_coordinates(latitude = 38.845985,
                                                  longitude = -76.92744)

3. Work with the Results
===============================

Work with Python Objects
---------------------------

.. code-block:: python

  location.matched_address

  >> 4600 SILVER HILL RD, WASHINGTON, DC 20233

For detailed documentation, please see the
`complete documentation <https://census-geocoder.readthedocs.org/en/latest.html>`_

---------------


*********************
Questions and Issues
*********************

You can ask questions and report issues on the project's
`Github Issues Page <https://github.com/insightindustry/census-geocoder/issues>`_

-----------------

*********************
Contributing
*********************

We welcome contributions and pull requests! For more information, please see the
`Contributor Guide <https://census-geocoder.readthedocs.io/en/latest/contributing.html>`_.

-------------------

*********************
Testing
*********************

We use `TravisCI <http://travisci.org>`_ for our build automation and
`ReadTheDocs <https://readthedocs.org>`_ for our documentation.

Detailed information about our test suite and how to run tests locally can be
found in our `Testing Reference <https://census-geocoder.readthedocs.io/en/latest/testing.html>`_.

--------------------

**********************
License
**********************

The **Census Geocoder** is made available under an
`MIT License <https://census-geocoder.readthedocs.io/en/latest/license.html>`_.
