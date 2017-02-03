.. _gridftp:

Download with GridFTP
=====================

Installation
************

*globus-url-copy* additional program is needed to transfer files with GridFTP.

It is part of the 'globus-gass-copy-progs' package and can be installed using instructions below.

Debian and derivative
---------------------

Install the package with:

.. code-block:: bash

    sudo apt-get install globus-gass-copy-progs

RHEL and derivative
-------------------

You need to install EPEL repository:

.. code-block:: bash

    sudo yum install epel-release -y

then install the package with:

.. code-block:: bash

    sudo yum install globus-gass-copy-progs

Configuration
*************

To use GridFTP as default protocol, add ``protocol=gridftp`` parameter in ``default.txt`` file.

.. note::

    ``default.txt`` file location differs depending on which synda installation method has been used: ``$ST_HOME/conf/default/default.txt`` for source installation and ``/etc/synda/sdt/default/default.txt`` for system package installation.


Usage
*****

Download a file using GridFTP protocol:

.. code-block:: bash

    synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 pastureFrac protocol=gridftp

Print GridFTP URL for a given file:

.. code-block:: bash

    synda dump cmip5.output1.MPI-M.MPI-ESM-LR.1pctCO2.day.atmos.cfDay.r1i1p1.v20120314.albisccp_cfDay_MPI-ESM-LR_1pctCO2_r1i1p1_19700101-19891231.nc limit=1 protocol=gridftp replica=false -nf -C url

Print a random GridFTP URL:

.. code-block:: bash

    synda dump data_node=bmbf-ipcc-ar5.dkrz.de limit=1 protocol=gridftp -nf -C url

Print a list of GridFTP URLs:

.. code-block:: bash

    synda dump protocol=gridftp variable=tas limit=1000 -f -C url

.. note ::

    In this last example, the command returns a mix of GridFTP and HTTP URLs. This is because when GridFTP protocol is not available, HTTP protocol is used instead.
