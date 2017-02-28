.. _user-guide-sdw:

Worker User Guide
=================

Introduction
************

A Python daemon (whom we call a “worker”) deals with the database using a Remote Procedure Call (RPC) client skeleton.
For any waiting job the worker inputs the corresponding (atomic) dataset to each process.
Any transition with waiting status is handle by the worker that forks a Shell child-process or loads a Python script as
module, accordingly to the job. Finally the worker returns the job status and updates the corresponding database entry
to reach the next transition. No more jobs appears when all atomic datasets and datasets reach the done status.

Configuration
*************

 - Edit ``synda_wo`` and set the :ref:```sdp`` service password <config-param-ref-sdp>` as global variable.

Test
****

Test communication between ``sdw`` and ``sdp``

.. code-block:: bash

    synda_wo -t -v

Usage
*****

.. code-block:: bash

    usage: synda_wo_dev [-h] [-d] [-H <host>] [-P <port>] [-j <job_class>]
                        [-l <logdir>] [-p <pipeline>] [-s <path>] [-t]
                        [-T <timeout>] [-u <user>] [-g <group>] [-1] [-v] [-V]
                        [{start,stop,status}]

    Post-processing worker used to fork Shell child-process or load python script as module.
    The worker deals
                with sdp database from synchro-data to input CMIP5 variable to each process.
    The worker returns job status
                to the database with run_log.

    This script contains RPC client skeleton.

    positional arguments:
      {start,stop,status}

    optional arguments:
      -h, --help           show this help message and exit
      -d, --debug          Debug mode
      -H <host>            Remote service hostname
      -P <port>            Remote service port
      -j <job_class>       Only processes specified job class.
                           Multiple values can be set using comma as delimiter.
      -l <logdir>          Logfile directory
      -p <pipeline>        Only processes specified pipeline.
      -s <path>            Process script directory
      -t, --test           Test server connection
      -T <timeout>         Remote service timeout
      -u <user>            Unprivileged user
      -g <group>           Unprivileged group
      -1, --one-item-only  Apply process on only one database entry
      -v, --verbose        Verbose mode
      -V, --version        Program version

Error management
****************

Getting information about errors
--------------------------------

Log files below contain useful information about errors:

- ``worker.log`` contains information regarding the worker execution.

.. note::

    If no ``-l`` flag, log files are stored in ``$HOME/sdw/log`` folder (source installation) and ``/var/log/synda/sdw`` folder (system package installation).

