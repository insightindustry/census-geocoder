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
       | * `Requests v.2.26 <https://docs.python-requests.org/en/master/>`_ or higher

-------------

************************************
Why the Census Geocoder?
************************************

In fulfilling its constitutional and statutory obligations, the US Census Bureau provides
extensive data about the United States. They make this data available publicly through
their website, through their raw data files, and through their APIs. However, while their
public APIs provide great data, they are limited in both tooling and documentation. So to
help with that, we've created the **US Census Geocoder** library.

The **Census Geocoder** library is designed to provide a Pythonic interface for
interacting with the Census Bureau's
`Geocoder API <https://geocoding.geo.census.gov/geocoder/>`_. It is specifically designed
to eliminate the scaffolding needed to query the API directly, and provides for simpler
and cleaner function calls to return forward geocoding and
reverse geocoding information. Furthermore, it exposes Python object
representations of the outputs returned by the API making it easy to work with the API's
data in your applications.


**************************************
Key US Census Geocoder Features
**************************************

* **Easy to adopt**. Just install and import the library, and you can be
  forward geocoding and reverse geocoding with just two lines of code.
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

* Supports all available benchmarks, vintages, and layers.
* Simplified syntax for indicating benchmarks, vintages, and layers.
* No more hard to interpret field names. The library uses simplified (read: human
  understandable) names for location and geography properties.

------------------

*********************************
Hello World and Basic Usage
*********************************

1. Import the Census Geocoder
================================

.. code-block:: python

  import census_geocoder as geocoder

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

  location.matched_addresses[0].address

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
