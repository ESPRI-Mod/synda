.. _overview:

Synda overview
==============

Synopsis
########
This document describes how to search and download files from ESGF archives with Synda.

General
########
Synda downloads files using HTTP protocol.

Search criteria called facets are used to select which files to download.

Search criteria can be set on command line
.. code-block:: bash

    synda search atmos fx CMIP5

or stored in a file

    synda search -s FILE

Usage
########
To list facets

.. code-block:: bash

    synda param

To list facet values

.. code-block:: bash

    synda param FACET

To search datasets

.. code-block:: bash

    synda search FACET..

To download a dataset

.. code-block:: bash

    synda get DATASET

To download a dataset with tracking info

.. code-block:: bash

    synda install DATASET

See also
########
* [User Guide](user_guide.rst)
* [Download Tutorial](download_tutorial.rst)
