.. _src-install-sdt:

Installation from conda
=======================

Requirements
************

Linux distribution with Python 3.8+.

A local file system should be preferred over a parallel distributed file system for the database file.

Installation
************

Then install ``synda`` package using command below:

.. code-block:: bash

    conda update -c ipsl -c conda-forge synda

Configuration
*************

- Add lines below in your shell configuration file (e.g. ``.bashrc``)

.. code-block:: bash

    export ST_HOME=$HOME/sdt
    export PATH=$ST_HOME/bin:$PATH

- Edit ``$ST_HOME/conf/credentials.conf`` file

.. note::

    To download file from ESGF, you need to untar an openID account on one ESGF identity provider website (e.g. PCMDI, BADC, DKRZ.) and subscribe to the project licence/role you want to download.

- A quickstart guide is available with

.. code-block:: bash

    synda intro | more

Files location
**************

.. code-block:: bash

    $HOME/sdt/doc
    $HOME/sdt/bin
    $HOME/sdt/conf
    $HOME/sdt/data
    $HOME/sdt/db
    $HOME/sdt/log
    $HOME/sdt/tmp
    $HOME/sdt/tmp/.esg
    $HOME/sdt/tmp/.esg/certificates
