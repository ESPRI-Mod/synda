.. _user-guide-sdt:

User Guide
==========

Introduction
************

There are two ways of downloading data with Synda: using ``synda get`` command, and using ``synda install`` command.
``synda get`` is similar to ``wget`` command while ``synda install`` is similar to ``apt-get`` command (but asynchronous).
``synda get`` is handy to quickly download a few files, while ``synda install`` is intended to manage a large number of files.
The differences between ``synda get`` and ``synda install`` are listed below:

``synda get``:
- no tracking
- no parallel download
- no daemon involved
- synchronous

``synda install``:
- tracking
- parallel download
- use daemon to manage download
- asynchronous

``synda search``
****************

Search criteria called facets are used to select which files to download. Search criteria can be set on command line first:

.. code-block:: bash

    synda search atmos fx CMIP5

or stored in a file:

.. code-block:: bash

    synda search -s <selection-file>

``synda param``
***************

To list facets:

.. code-block:: bash

    synda param

To list facet values:

.. code-block:: bash

    synda param <facet-key>

To search datasets on-the-fly:

.. code-block:: bash

    synda search <facet-value>

``synda get``
*************

.. code-block:: bash

    synda get [ ID ] [ FACET ]...

The downloaded file(s) are stored in the :ref:`sandbox directory <config-param-ref-sdt>`. A different folder can be specified using ``-d`` option.

Download a dataset:

.. code-block:: bash

    synda get cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601

Download a file:

.. code-block:: bash

    synda get orog_fx_CanCM4_decadal1972_r0i0p0.nc

If download fails, you can search for another replica using ``-r`` option:

.. code-block:: bash

    synda search -r  [ ID ] [ FACET ]...

Then retry the download with the ``data_node`` parameter to specify which replica to use:

.. code-block:: bash

    synda search -r orog_fx_CanCM4_decadal1972_r0i0p0.nc

    synda get -f orog_fx_CanCM4_decadal1972_r0i0p0.nc data_node=esgf2.dkrz.de 

``synda install``
*****************

.. code-block:: bash

    synda install [ ID ] [ FACET ]...

This command adds matching file(s) in the download queue and store tracking information in the local database.

A background process checks the download queue regularly and download the files.

The downloaded files are stored in the :ref:`data directory <config-param-ref-sdt>`.

Install a dataset:

.. code-block:: bash

    synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529

Install a variable:

.. code-block:: bash

    synda install cmip5.output1.CSIRO-BOM.ACCESS1-3.abrupt4xCO2.day.atmos.day.r1i1p1.v1 tas

Install a file:

.. code-block:: bash

    synda install cmip5.output1.CNRM-CERFACS.CNRM-CM5.rcp85.fx.atmos.fx.r0i0p0.v20130826.sftlf_fx_CNRM-CM5_rcp85_r0i0p0.nc

Install files matching facets stored in a :ref:`selection file <selection-file>`:

.. code-block:: text

    project=CMIP5
    model=CNRM-CM5 CSIRO-Mk3-6-0
    experiment=historical amip
    ensemble=r1i1p1
    variable[atmos][mon]=tasmin tas psl
    variable[ocean][fx]=areacello sftof
    variable[land][mon]=mrsos nppRoot nep

.. code-block:: bash

   synda install -s sample_selection_01.txt

Start/Stop downloading
**********************

In source installation, run command below:

.. code-block:: bash

    synda download [ start | stop ]

Error management
****************

Changing replica for all file in errors
---------------------------------------

If download fails you can try another replica.

To change the replica for all files in error, use command below:

.. code-block:: bash

    synda replica next

Getting information about errors
--------------------------------

Log files below contain useful information about errors:

- ``discovery.log`` contains information regarding discovery.
- ``transfer.log`` contains information regarding download.
- ``debug.log`` contains low-level download information.

.. note::

    Log files are stored in ``$HOME/log`` folder.
