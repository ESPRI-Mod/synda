.. _download:

Basic download
==============

A session might go like:

Set ESGF openid and password in `credentials.conf`.

.. code-block:: bash

    vi credentials.conf

Search a dataset:

.. code-block:: bash

    $ synda search CMIP5 decadal1995 mon land
    new  cmip5.output1.CCCma.CanCM4.decadal1995.mon.land.Lmon.r2i2p1.v20120608
    new  cmip5.output1.CCCma.CanCM4.decadal1995.mon.land.Lmon.r8i2p1.v20120608
    new  cmip5.output1.MIROC.MIROC4h.decadal1995.mon.land.Lmon.r5i1p1.v20120628
    new  cmip5.output1.MRI.MRI-CGCM3.decadal1995.mon.land.Lmon.r5i1p1.v20110915
    [...]

List dataset variables:

.. code-block:: bash

    $ synda search -v cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529
    cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.baresoilFrac.v20120529.aggregation
    cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.burntArea.v20120529.aggregation
    cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.c3PftFrac.v20120529.aggregation
    [...]

List file(s) for a specific variable:

.. code-block:: bash

    $ synda search -f cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
    new  8.9 MB  cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529.baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc

Mark the file for download:

.. code-block:: bash

    $ synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
    1 file(s) will be added to the download queue.
    Once downloaded, 8.9 MB of additional disk space will be used.
    Do you want to continue? [Y/n] 
    1 file(s) enqueued

Start the daemon:

.. code-block:: bash

    $ synda daemon start

Check download progress:

.. code-block:: bash

    $ synda queue
    status      count  size
    running         1  8.9 MB

    $ synda watch
    Current size    Total size    Download start date         Filename
    8.9 MB          8.9 MB        2015-12-15 10:31:53.848936  baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc

    $ synda queue
    status      count  size
    done            1  8.9 MB

.. code-block:: bash

    $ find data -type f
    data/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc


To debug certificate issue, you can use:

.. code-block:: bash

    $ synda certificate renew

To debug file transfer error, you can use:

.. code-block:: bash

    $ synda get <file_url>
