.. _replication-sdt:

ESGF replication
================

Introduction
************

This document describes how to create an ESGF archives partial mirror on a local cluster and keep it up to date.

Synda installation
******************

See synda installation from :ref:`RPM package <rpm-install-sdt>`, :ref:`DEB package <deb-install-sdt>` or :ref:`sources <src-install-sdt>`.

Create a selection file to describe which data to replicate
***********************************************************

See :ref:`the selection file section <selection-file>`

.. note::

    You can create many selection files (e.g. one per project). Selection file(s) must be stored in the "selection" folder.

File discovery
**************

Install your selection file:

.. code-block:: bash

    synda install -s <selection-file>

Or upgrade the file discovery:

.. code-block:: bash

    synda upgrade

At this point, files metadata are stored in local database and data download can begin.

Files download
**************

Start
-----

To start the download, in single-user installation, run command below:

.. code-block:: bash

    synda daemon start

In multi-user installation, run command below:

.. code-block:: bash

    service sdt start

Stop
----

To stop the download, in single-user installation, run command below:

.. code-block:: bash

    synda daemon stop

In multi-user installation, run command below:

.. code-block:: bash

    service sdt stop

Watching download progress
**************************

Commands below give download status and progress:

.. code-block:: bash

    synda queue
    synda watch

Update datasets to the latest version
*************************************

In ESGF, a dataset can change over time and thus have several versions. Re-run the discovery to search for new versions:

.. code-block:: bash

    synda upgrade

Then start the Synda service to start the download of new versions if any.

Remove old datasets version
***************************

Run command below:

.. code-block:: bash

    synda autoremove

Error management
****************

Errors can occur during download for different reasons: remote server is
down, incorrect files access right, authorization issue, authentication
issue, etc.

Displaying errors
-----------------

Command below can be used to print how many error occured

.. code-block:: bash

    synda queue

Retrying download in errors
***************************

Command below can be used to retry transfer(s) in error:

.. code-block:: bash

    synda retry

.. note::

    crontab can be used to retry errors (e.g. every day).

Changing replica for all files in errors
****************************************

Sometime, current file replica always fails as the remote server is
down. One way to solve the problem is to change the file replica.

To change the replica for all files in error, use command below:

.. code-block:: bash

    synda replica next

Getting more details about errors
*********************************

Log files below contain useful information about errors:

- ``discovery.log`` contains information regarding discovery.
- ``transfer.log`` contains information regarding download.
- ``debug.log`` contains low-level download information.

.. note::

    Log files are stored in ``$HOME/sdt/log`` folder (single-user installation) and ``/var/log/synda/sdt`` folder (multi-user installation).
