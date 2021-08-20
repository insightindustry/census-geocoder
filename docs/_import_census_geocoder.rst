Importing the **Census Geocoder** is very straightforward. You can either import its
components precisely (see :doc:`API Reference <api>`) or simply import the entire module:

.. code-block:: python

  # Import the entire module.
  import census_geocoder as geocoder

  result = geocoder.location.from_address('4600 Silver Hill Rd, Washington, DC 20233')
  result = geocoder.geography.from_address('4600 Silver Hill Rd, Washington, DC 20233')

  # Import precise components.
  from census_geocoder import Location, Geography

  result = Location.from_address('4600 Silver Hill Rd, Washington, DC 20233')
  result = Geography.from_address('4600 Silver Hill Rd, Washington, DC 20233')
