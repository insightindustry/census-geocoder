Retrieving data about canonical locations is very straightforward. You have four different
ways to get this information, depending on what information you have about the location
you want to geocode:

.. tabs::

  .. tab:: Single-line Address

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_address('4600 Silver Hill Rd, Washington, DC 20233')

    .. seealso::

      * :meth:`Location.from_address() <census_geocoder.locations.Location.from_address>`

  .. tab:: Parametrized Address

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_address(street = '4600 Silver Hill Rd',
                                              city = 'Washington',
                                              state = 'DC',
                                              zip_code = '20233')

    .. seealso::

      * :meth:`Location.from_address() <census_geocoder.locations.Location.from_address>`

  .. tab:: Coordinates

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_coordinates(longitude = -76.92744,
                                                  latitude = 38.845985)

    .. seealso::

      * :meth:`Location.from_coordinates() <census_geocoder.locations.Location.from_coordinates>`

  .. tab:: Batch File

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.location.from_batch(file_ = '/my-csv-file.csv')

    .. caution::

      The batch file indicated can have a maximum of 10,000 records.

    .. warning::

      While the `Census Geocoder API`_ supports CSV, TXT, XLSX, and DAT formats the
      **Census Geocoder** library only supports CSV and TXT formats so as to avoid
      dependency-bloat (read: Why rely on other libraries to read XLSX format data?).

    .. seealso::

      * :meth:`Location.from_batch() <census_geocoder.locations.Location.from_batch>`
