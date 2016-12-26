#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains messages available as string."""

m0001="search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted."

def m0003(host):
    return """Request sent to %s. Please wait.."""%host
    #return """%s contacted. Waiting for reply.."""%host

def m0004(prog):
    return """  %s
  %s mo
  %s model
  %s model MR"""%((prog,)*4)

m0005="""
  If 'localsearch' option is false (default), search in ESGF archive.

  If 'localsearch' option is true, search in local repository.

  Without search filters, all records are returned.

  Filter name can be omitted (i.e. 'atmos' can be used intead of 'realm=atmos').

  For ease of use, limit can be set directly on the command line as a simple number (i.e. the number of row(s) to return)
"""

def m0006(name,description,example=None,note=None):
    import StringIO                                                                                                                              
    buf = StringIO.StringIO()                                                                                                                    
    buf.write("%s\n%s\n"%(name,description))
    if example is not None:
        buf.write("\nExample\n%s\n"%example)
    if note is not None:
        buf.write("\nNotes\n%s\n"%note)
    return buf.getvalue()

m0007='delete cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926.ua_6hrLev_MIROC4h_rcp45_r1i1p1_2029081100-2029082018.nc'
m0008='add cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926.ua_6hrLev_MIROC4h_rcp45_r1i1p1_2029081100-2029082018.nc'
m0009="<file> format follow Search-API 'instance_id' attribute."
m0010="""
            retry all
            retry cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926.ua_6hrLev_MIROC4h_rcp45_r1i1p1_2029081100-2029082018.nc
"""

m0011="""
        set                  Show all session parameters that differ from default values.
        set all              Show all session parameters.
        set option           Show all options
        set facet            Show all facets
        set default          Reset all session parameters
        set name=value       Set <name> to <value>
        set {name}?          Show session parameter value
        """

m0012="""
            daemon start
            daemon stop
            daemon status
        """

m0013="""
            sample small_dataset
            sample remote
            sample local
        """

m0014="""
            selection list [ filter ]
            selection edit <idx>
            selection cat <idx>
            selection print <idx>
        """

m0015="""
Synda subcommands list

"""

m0016="synda - a fast and versatile data management tool for Earth Science Grid Federation (ESGF)"

m0017="action"

m0018="""
Mailing list:

esgf-user@lists.llnl.gov

Email:

sdipsl@ipsl.jussieu.fr

Website:

https://github.com/Prodiguer/synda
"""

m0019="""
Introduction to synda command

A session might go like

Set ESGF openid and passwd in credentials file:

vi $HOME/sdt/conf/credentials.conf

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

The file should be available in $HOME/sdt/data

$ find $HOME/sdt/data -type f
/home/foo/sdt/data/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc


In case something goes wrong, you can check the logfiles in $HOME/sdt/log for
information about the error.


To debug file transfer error and certificate issue, you can use the two
commands below:

$ synda certificate renew

(to test certificate renewal)

and 

$ synda get <file_url>

(to test file download)
"""

m0020="""
This may be caused by a typo in search parameters, or by the cache containing outdated informations.
To refresh the cache, run 'synda update' command.
"""

m0021="""
This may be caused by a typo in the search parameters, or by the cache containing outdated informations.
To refresh the cache, run 'synda update' command.
You can also disable parameters checking by setting 'check_parameter=0' in configuration file.
"""

m0022="""  'install' command is asynchronous, the transfer is handled by a
  background process. To check when the download is complete, use 'synda 
  queue' command.
"""

m0023="""  This command is for source installation only (in system package
  installation, Synda daemon is installed as a service and is managed
  using 'service' command).
"""

m0024="""Set the total number of returned results. By default, returns the first 100 records matching the given constraints. Limit can be also be changed through the keyword parameters limit=. The system imposes a maximum value of limit <= 10,000."""

m0025="""sudo service synda start"""

m0026="""synda daemon start"""

m0027="You must either be root, or part of the synda group to perform this command."
