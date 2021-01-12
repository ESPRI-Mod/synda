# Download Tutorial

A session might go like

Set ESGF openid and passwd in [*credentials file*](files.md#credentialsconf):

    vi credentials.conf

Search a dataset:

    $ synda search CMIP5 decadal1995 mon land
    new  cmip5.output1.CCCma.CanCM4.decadal1995.mon.land.Lmon.r2i2p1.v20120608
    new  cmip5.output1.CCCma.CanCM4.decadal1995.mon.land.Lmon.r8i2p1.v20120608
    new  cmip5.output1.MIROC.MIROC4h.decadal1995.mon.land.Lmon.r5i1p1.v20120628
    new  cmip5.output1.MRI.MRI-CGCM3.decadal1995.mon.land.Lmon.r5i1p1.v20110915
    ..

List dataset variables:

    $ synda search -v cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529
    cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.baresoilFrac.v20120529.aggregation
    cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.burntArea.v20120529.aggregation
    cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.c3PftFrac.v20120529.aggregation
    ..

List file(s) for baresoilFrac variable:

    $ synda search -f cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
    new  8.9 MB  cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529.baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc

Mark the file for download:

    $ synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
    1 file(s) will be added to the download queue.
    Once downloaded, 8.9 MB of additional disk space will be used.
    Do you want to continue? [Y/n] 
    1 file(s) enqueued

Start the daemon

    $ synda daemon start

Check download progress:

    $ synda queue
    status      count  size
    running         1  8.9 MB

    $ synda watch
    Current size    Total size    Download start date         Filename
    8.9 MB          8.9 MB        2015-12-15 10:31:53.848936  baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc

    $ synda queue
    status      count  size
    done            1  8.9 MB

The file should be available in [*data folder*](files.md#data)

    $ find data -type f
    data/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc

In case something goes wrong, you can check [*log files*](files.md#log)
for information about the error.

To debug certificate issue, you can use

    $ synda certificate renew

To debug file transfer error, you can use

    $ synda get <file_url>
