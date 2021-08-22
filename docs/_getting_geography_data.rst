Retrieving data about the geographic areas that contain a given location/place is just
as straightforward as :ref:`getting location data <geocoding_locations>`. In fact, the
syntax is almost identical. Just swap out the word ``'location'`` for ``'geography'``
and you're done!

Here's how to do it:

.. tabs::

  .. tab:: Single-line Address

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.geography.from_address('4600 Silver Hill Rd, Washington, DC 20233')

    .. seealso::

      * :meth:`GeographicEntity.from_address() <census_geocoder.geographies.GeographicEntity.from_address>`

  .. tab:: Parametrized Address

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.geography.from_address(street = '4600 Silver Hill Rd',
                                               city = 'Washington',
                                               state = 'DC',
                                               zip_code = '20233')

    .. seealso::

      * :meth:`GeographicEntity.from_address() <census_geocoder.geographies.GeographicEntity.from_address>`

  .. tab:: Coordinates

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.geography.from_coordinates(longitude = -76.92744,
                                                   latitude = 38.845985)

    .. seealso::

      * :meth:`GeographicEntity.from_coordinates() <census_geocoder.geographies.GeographicEntity.from_coordinates>`

  .. tab:: Batch File

    .. code-block:: python

      import census_geocoder as geocoder

      result = geocoder.geographies.from_batch(file_ = '/my-csv-file.csv')

    .. caution::

      The batch file indicated can have a maximum of 10,000 records.

    .. warning::

      While the `Census Geocoder API`_ supports CSV, TXT, XLSX, and DAT formats the
      **Census Geocoder** library only supports CSV and TXT formats so as to avoid
      dependency-bloat (read: Why rely on other libraries to read XLSX format data?).

    .. seealso::

      * :meth:`GeographicEntity.from_batch() <census_geocoder.geographies.GeographicEntity.from_batch>`
