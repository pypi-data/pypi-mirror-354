========================
CTI DB Python Module
========================

Description
-----------

This is a Python module for reading CTI DB files.

CTI DB is a binary file format that stores data indexed by IP address
subnets (IPv4 only).

Installation
------------

To install ctidb, simply:

.. code-block:: bash

    $ pip install ctidb

Usage
-----

To use this module, you must first download or create a CTI DB file.

After you have obtained a database and imported the module, call
``CCtiReader`` with a path,
to the database as the first argument. Optionally, you may pass a mode as the
second argument. The modes are exported from ``ctidb``. Valid modes are:

* ``MODE_MEMORY`` - load database into memory. Pure Python.
* ``MODE_AUTO`` - Default.

**NOTE**:
To look up an IP address, use the ``get`` method on this object. The method will return the
corresponding values for the IP address from the database (e.g., a dictionary
for GeoIP2/GeoLite2 databases). If the database does not contain a record for
that IP address, the method will return ``None``.

Example
-------

.. code-block:: pycon

    >>> import ctidb
    >>>
    >>> with ctidb.CCtiReader('criminalip.ctidb') as reader:
    >>>
    >>>     reader.get('223.26.31.75')
    {'country': ... }

Exceptions
----------

The module will return an ``InvalidDatabaseError`` if the database is corrupt
or otherwise invalid. A ``ValueError`` will be thrown if you look up an
invalid IP address or an IPv6 address in an IPv4 database.

Requirements
------------

This code requires Python 3.7+. Older versions are not supported.

Versioning
----------



Support
-------
