.. _user-guide-sdp:

User guide
==========

Introduction
************

Synda Post-Processing module is used to transform ESGF data files. In the centre is a "pipeline" database that list individual jobs to be run.
These jobs are claimed and processed by Workers - autonomous processes that are running on the compute farm and connect
to the pipeline database to report about the progress of Jobs or claim some more. When a Worker discovers that
its predefined time is up or that there are no more Jobs to do, it claims no more Jobs and exits the compute farm
freeing the resources. Thus, Synda allows a parallel, orderly and asynchronous post-processing on each tracked dataset.

Configuration
*************

``sdt`` module
--------------

Set ``post_processing`` parameter to ``true`` in ``$ST\_HOME/conf/sdt.conf``:

.. code-block:: text

    post_processing=true

``sdp`` module
--------------


- Edit ``/etc/synda/sdp/credentials.conf`` file to configure the RPC server:

.. code-block:: text

    [rpcserver]
    username=xxxxxx
    password=xxxxxx


- :ref:`Edit configuration file <config-param-ref-sdp>`.

- :ref:`Declare your pipelines and bindings <pipeline-file>`.

Start post-processing
*********************

In source installation, run command below:`

.. code-block:: bash

    synda_pp daemon start

In system package installation, run command below:

.. code-block:: bash

    service sdp start

Start ``sdw`` service
*********************

When all the events are sent from ``sdt`` to ``sdp`` and all corresponding post-processing entries are created into ``sdp.db`` pending for execution by a :ref:`Synda Worker <user-guide-sdw>`.

This is the client side post-processing daemon (aka "worker"). To start the service, run command below:

.. code-block:: bash

    synda_wo --script_dir /your/scripts start

Communication test between modules
**********************************

Test communication between ``sdt`` and ``sdp``

.. code-block:: bash

    $ST_HOME/lib/sd/sdppproxy.py -v

If tests failed, check if credentials and are :ref:```sdp.conf`` <config-param-ref-sdp>` are correctly set then restart the services.

Example
*******

Let's download a file:

.. code-block:: bash

    synda install -y sfcWind_ARC-44_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4-SN_v1_sem_197012-198011.nc

After a few minutes, the file should have been transferred and the jobs should have been triggered.

To check the result, let's see the logfile:

.. code-block:: bash

    vi $SP_HOME/log/worker.log

If all went well, the logfile should look like this:

.. code-block:: bash

    2017/01/10 09:09:56 AM INFO Processing job (transition=task_A,args={u'pipeline': u'P001', u'data_folder': u'/home/jerome/sdp/data', u'project': u'CORDEX', u'variable': u's
    fcWind', u'model': u'RCA4-SN', u'dataset_pattern': u'cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123'},job_class=foo,start_date=2017-01-10 09:09:56.791281,ppprun_id=1,error_msg=None)
    2017/01/10 09:09:56 AM DEBUG Script return code: 0
    2017/01/10 09:09:56 AM DEBUG Script stdout:
    2017/01/10 09:09:56 AM DEBUG Script stderr:
    2017-01-10 09:09:56 - INF001 - task_A.sh script started
    2017-01-10 09:09:56 - INF002 - dataset_pattern: cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123
    2017-01-10 09:09:56 - INF003 - task_A.sh script ends.
    2017/01/10 09:09:56 AM INFO Processing job (transition=task_B,args={u'pipeline': u'P001', u'data_folder': u'/home/jerome/sdp/data', u'project': u'CORDEX', u'variable': u'sfcWind', u'model': u'RCA4-SN', u'dataset_pattern': u'cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123'},job_class=bar,start_date=2017-01-10 09:09:56.887659,ppprun_id=1,error_msg=None)
    2017/01/10 09:09:56 AM DEBUG Script return code: 0
    2017/01/10 09:09:56 AM DEBUG Script stdout:
    2017/01/10 09:09:56 AM DEBUG Script stderr:
    2017-01-10 09:09:56 - INF001 - task_B.sh script started
    2017-01-10 09:09:56 - INF002 - dataset_pattern: cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123
    2017-01-10 09:09:56 - INF003 - task_B.sh script ends.
    2017/01/10 09:09:57 AM INFO Processing job (transition=task_C,args={u'pipeline': u'P001', u'data_folder': u'/home/jerome/sdp/data', u'project': u'CORDEX', u'variable': u'sfcWind', u'model': u'RCA4-SN', u'dataset_pattern': u'cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123'},job_class=foobar,start_date=2017-01-10 09:09:56.985872,ppprun_id=1,error_msg=None)
    2017/01/10 09:09:57 AM DEBUG Script return code: 0
    2017/01/10 09:09:57 AM DEBUG Script stdout:
    2017/01/10 09:09:57 AM DEBUG Script stderr:
    2017-01-10 09:09:57 - INF001 - task_C.sh script started
    2017-01-10 09:09:57 - INF002 - dataset_pattern: cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123
    2017-01-10 09:09:57 - INF003 - task_C.sh script ends.

Error management
****************

Getting information about errors
--------------------------------

Log files below contain useful information about errors:

- ``daemon.log`` contains information regarding the daemon execution.
- ``stacktrace.log`` contains information regarding occurring errors.

.. note::

    Log files are stored in ``$HOME/sdp/log`` folder (source installation) and ``/var/log/synda/sdp`` folder (system package installation).


