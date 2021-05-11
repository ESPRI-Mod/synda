.. _log:

Changelog
=========

Transfer Module
***************
Version 3.4 - 2021-xx-xx
    - enhancement
        - downloads are performed asynchronously, using only one protocol (http) and under the control of asyncio
        - std.conf new entries : big_file_size, big_file_chunksize
        - internal.conf entry : transfer_protocol
    - tests :
        - remove subcommand : new data file embedded is ten times smaller than previous one
    - deprecated features
        - gridftp protocol
        - wget http client
        - std.conf entries : gridftp_opt
        - internal.conf entry : transfer_protocols
        - documentation update
Version 3.35 - 2021-05-07
    - bug correction :
        - init-env subcommand now provides empty default selection files (see conf/default directory)
        - issue # 185 : 'synda remove' fails to import sdsimplefilter
Version 3.34 - 2021-04-02
    - bug correction :
        - Default selection file for CMIP6 project is now delivered empty. It can be customized under user control (issue # 178 : Dataset not found but available on ESGF web interface)
    - Documentation update
Version 3.33 - 2021-03-31
    - bug correction :
        - issue # 177 : synda now allows that ESGF openIDs are case sensitive
Version 3.32 - 2021-03-24 - (PYTHON 3)
    - enhancement
        - code migration : third attempt to migrate synda from python 2 to python 3  (success)
    - bug correction :
        - issue # 176 (conda channel changed : now : conda-forge [ipsl channel has been removed])
Version 3.31 - 2021-03-22
    - enhancement
        - code migration : second attempt to migrate synda from python 2 to python 3 (failure)
    - bug correction :
        - issue # 168 (Master branch update broke sdnexturl.py)
Version 3.30 - 2021-03-22
    - enhancement
        - code migration : first attempt to migrate synda from python 2 to python 3 (failure)
    - bugs correction :
        - synda -h and synda -V sub-commands are now operational
    - deprecated features
        - 'open' subcommand
        - packages : sdpoodlefix, sdxml, sdhtmlbasic, sdselectionfile, sdview
Version 3.2 - 2021-01-11
    - config parameters externalisation

      - 'sdt.conf' file has new customizable parameters
      - New 'internal.conf' file, for advanced parameters (not customizable, located into the /conf directory)
    - enhancements

      - init-env subcommand is enabled to build user environment
      - synda raises on the command line the problems encountered by esgf_search api service
      - In sdparam.get_name_from_value method, if more than one match, the print message has now a 'info' level
      - store stacktrace log files in /log directory.

    - bugs correction :

      - help subcommand can be used even if user has not built yet any environment

    - deprecated features

      - 'pexec' subcommand
      - 'thredds_catalog' & 'apache_default_listing' APIS (synda operates only the 'esgf_search' API)
      - synda ihm
      - packages : sdevent, sdeventdao, sddatasetpattern, sdoperation


Version 3.15 - 2020-11-17
    - cleaning & packages reorganization
    - issue #158 - bug correction - daemon stopping without reporting errors
Version 3.14 - 2020-10-29
    - new files encoding : ISO-8859-1 => utf8
Version 3.13 - 2020-10-28
    - entry point moved to setup.py instead of meta.yaml file
Version 3.9 - 2017-02-19
    - add gridftp_opt option in sdt.conf.
    - dataset attributes can be used in 'local_path_drs_template'.
    - use decimal prefix instead of binary prefix in 'synda metrics' command.
    - do not include checksum computation time in download time metric.
    - enable supplementary groups support if available.
Version 3.8 - 2017-02-19
    - add ``info`` action to ``synda certificate`` command
    - add security_dir_mode option
    - add subfolder to the ESGF certificate path (named after the user UID)
    - all deletions now occurs synchronously (deferred mode is disabled)
    - follow symlinks during ``synda remove`` operation
    - add manual routines to refresh dataset status
    - new cleanup algo for ``synda remove`` command (run faster)
    - add full path support in ``local_path_drs_template`` var
    - add write test in sddaemon module
    - store stacktrace file in /tmp
    - add uuid to stacktrace file name
    - move try/except block upstream to enclose the daemon context
    - fix permission in sys-pkg for ``/srv/synda/sdt`` folder (g+sw)
Version 3.7 - 2017-01-15
    - ESGF certificate path set to $HOME/sdt/tmp/.esg for source install.
    - disable sdfilepermission module.
    - add user personal env (SDT_USER_ENV).
    - synda group can be used instead of sudo (system package).
    - set specific version for pillow package.
    - bugfixes.
Version 3.6 - 2016-12-04
    - use search-api json format instead of xml
    - add end-of-transfer events replay mode (trigger all EOT events in batch mode)
    - add ``synda count`` subcommand
    - add ``synda config`` subcommand
    - add incremental mode for discovery operation
    - add dataset version consistency check
Version 3.5 - 2016-09-19
    - use requests (pypi) to resolve openid
    - add ``~/.sdt/conf/credentials.conf``
    - add ``~/.sdt/conf/sdt.conf``
    - remove ``~/.syndarc``
    - add ``open`` subcommand
    - add ``check`` subcommand for selection
    - add ``check`` subcommand for file's variable
    - use myproxyclient latest version
    - add ``default_path`` option in sdt.conf
    - use sdpyproxy python module to renew X509 certificate (replace obsolete sdlogon.sh script)
    - change tarball location for source installation (use install.sh latest version)
    - replace argparse RawTextHelpFormatter with RawDescriptionHelpFormatter
    - set ``metadata_parallel_download`` to False
    - add support for lowmem machine
    - add sdsqlitedict module
    - add sdmts module
    - add ``ignorecase`` filter for ``upgrade`` and ``facet`` subcommands
    - remove ``-n`` option from ``synda facet`` subcommand
    - do not stop daemon anymore when error occurs during download (except for certificate renewal error)
    - always print stacktrace when error occurs (ST_DEBUG env. var. is not used anymore)
    - write yes/no confirmation message on stderr
    - prevent adding predefined values for ``version`` facet in local cache
    - add checksum type normalization routine
    - add ``url_replace`` selection file parameter
    - add ``http_fallback`` option (switch protocol on error)
    - add ``default_listing_size`` configuration option
    - add ``-m`` option to ``synda remove`` subcommand
    - ergonomy improvements
Version 3.4 - 2016-05-04
    - add ``synda variable`` subcommand
    - add ``synda get`` subcommand
    - remove ``synda test`` subcommand (``synda test`` is replaced by ``synda get``)
    - add urllib2 based download impl
    - add sandbox folder for untracked data
    - set data folder default value to /srv/synda/sdt/data (system package installation only)
    - disable parameter checking by default
    - insert event in db even if post-processing module is disabled
    - improve obs4MIPs project support
    - user documentation reorganization
    - add parameter reference documentation
    - add commands reference documentation
    - add selection file documentation
Version 3.3 - 2016-04-04
    - localpath DRS can be customized by user in configuration file (local_path_drs_template)
    - add hpss configuration parameter to retry transfer on error
    - add index_host and project options to the ``synda update`` subcommand
    - add examples for each subcommands
    - use argparse.RawTextHelpFormatter in subcommand help
    - add globus online support
    - set gridftp port range to 50000-51000
    - in sdget.sh and sdgetg.sh, ``-v`` option replace ``-d`` option (verbose replace debug_level)
    - add new ``value`` format for synda dump ``-F`` option
    - enable debug mode when using synda test <url> subcommand
    - ``synda list`` now list everything by default
    - add missing initialization in install.sh (g__transfer=0)
    - add configuration file documentation
    - move post_processing parameter from daemon section to module section
    - rename configuration file ``[path]`` section to ``[core]`` section
    - do not remove ca certs when using ``synda certificate renew`` option
    - add ``force_renew_ca_certficates`` option to remove ca certs
    - remove ``cache`` subcommand
    - remove ``sdreducecol`` filter from sdfilepipeline module
    - fix ``pkg_resources.DistributionNotFound: setuptools>=1.0`` bug
    - move common method from Dataset and File class to BaseType class
    - set ``prevent_daemon_and_modification`` to false for source installation
    - move ``max_parallel_download`` from ``[daemon]`` to ``[download]`` section
    - untar ihm_pid_file only if mutually exclusive lock is enabled
    - increase daemon sqlite timeout from 120s to 12000s
    - do not parse wget output by default and increase wget ``--tries`` to prevent hpss failure
    - default indexes set to dkrz
    - daemon non-privileged mode
Version 3.2 - 2016-02-03
    - DEB package
    - retrieve dataset timestamp in batch mode
    - modify Synda scheduler to ease Globus Online integration
    - prevent normal user to run admin commands in multi-user mode
    - set model attribute as optional
    - improve documentation
Version 3.1 - 2015-12-29
    - multi-user
    - daemon integrated in systemd
    - RPM package
    - per-user config file (~/.syndarc)
    - online help
    - parameter discovery (list parameter based on other parameters)
    - support for free syntax in template (e.g. [realm experiment frequency]=v1 v2)
    - default indexes set to pcmdi9
    - add inline tutorial
    - ``-z`` option replace ``-y`` option
    - ``-y`` option replace ``-N`` option
    - ``--yes`` option replace ``--non-interactive`` option
    - openid/passwd moved from sdt.conf to credentials.conf
    - add check to prevent normal user from running synda in write mode
    - add ignorecase filter
Version 3.0 - 2015-03-25
    - add new local search filter (status, error_msg)
    - add ``--version`` option to print version in synda command
    - improve external files support
    - add ``next replica`` action (batch mode)
    - move default selection files in ``sdt/conf/default``
    - move configuration file in ``sdt/conf`` folder
    - add ``history`` subcommand
    - move lfae_mode into sdt.conf
    - gridftp support
Version 2.9 - 2014-11-03
    - several template parameters names changed (e.g. tablename is now named cmor_table). See sdconvert.sh for more info
    - new synda command (apt-get like front-end)
    - support for most search-API parameters
    - "not" operation support (e.g. all models but one)
    - multi-DRS support
    - new formatting keyword
    - only localpath is mutable
    - support for different name for the same model (e.g. GFDL-CM2p1, GFDL-CM2.1 et GFDL-CM2-1)
    - default values per project
    - new ``searchapi_host`` parameter to specify which index to use
    - space are supported (e.g. "ISI-MIP Fasttrack")
    - replica support
    - wildcard (all/\_*) supported in all facets
    - local database reorganization
Version 2.8 - 2013-12-20
    - set CHUNKSIZE (search-API limit parameter) to 10000 (was 1000)
    - add time coverage filter
    - add support for ``sha256`` checksum type
Version 2.7 - 2013-08-20
    - fix B0039 bug
    - fix B0034 bug
    - fix B0033 bug
    - add EUCLIPSE project
    - XML parsing module rewriting
    - add "timeout/retry" mechanism in the discovery process
    - models discovery module improvement
    - move tuning parameters into configuration file
    - increase thredds-catalog timeout from 10 to 100
    - add second logger for domain/functional messages
    - load readonly tables in memory to speed up the discovery process
    - add CMOR tables cache system
    - add orphan transfer detection (without selection match)
    - ``stat`` subcommand rewriting
    - add db_path option in configuration file
Version 2.6 - 2013-04-18
    - add ``search-api-nocache`` discovery engine
    - add support for "obs4MIPs" project
    - add wild card support for realm and frequency
    - fix B0032 bug
Version 2.5 - 2012-12-18
    - add ``url`` column in dataset tmp tables
    - add ``-G`` option (remove tmp tables)
    - set ``MyProxyClient`` as default myproxy client
    - set search-API as default search-engine
    - add selection based statistics
    - add new ``-E`` option to retrieve model list from search-API
    - fix B0031 bug
    - replace PCMDI3 with PCMDI9 in get_data.sh script (myproxy server)
    - add search-API multithreading to run several search in parallel
    - add search-API call metrics (to trace time spent in each call)
    - add search-API pagination
    - fix B0030 bug
    - fix B0029 bug
    - fix B0028 bug
    - fix B0027 bug
    - fix B0026 bug
Version 2.4 - 2012-06-19
    - add ``-x`` option to run discovery process and print ESGF checksums
    - add ``-X`` option to control if local checksum match remote checksum
    - fix B0025 bug
    - add "latest" symlink creation routine (last version identifier)
    - add old versions suppression routine
    - add search API mode
    - add ``-L`` option (set ``latest`` flag)
    - fix B0024 bug
    - mark CSTE_TRANSFERT_STATUS_DELETED status as deprecated
Version 2.3 - 2012-04-20
    - add PROC0001 method to list obsolete version
    - add new columns latest_date and last_done_transfer_date
    - fix B0023 bug
    - fix B0022 bug (MIGR0001() method broken)
    - fix B0021 bug. (variable missing when retrieving transfert from database)
    - add ``-y`` option (dataset-info)
Version 2.2 - 2012-04-07
    - fix B0020 bug. (fix 2.2 at 20120410)
    - fix B0019 bug. (fix 2.2 at 20120407)
    - add ESGF MyProxyLogon (MyProxy Java client)
    - replace ``ps fax`` with ``ps ax`` (Mac port)
    - add dependencies check in install.sh
    - add transfer_helper modules
    - add dataset in transfer queue (eot_queue)
    - fix B0018 bug
    - fix B0017 bug
    - fix "[Error 98] address already in use"
    - use wget tries and timeout parameters from conf. file
    - fix B0016 bug
    - add ``-r`` option (exec proc)
    - use transfert_id instead of local_image as primary key (for update)
    - add new table ``dataset``
    - add new column ``dataset_id`` in transfer table
Version 2.1 - 2012-03-12
    - fix B0015 bug
    - add ``-V`` option in start.sh
    - add ``-b`` to myproxy-logon options (only if myproxy-logon >= 5.0)
    - set wget tries option to 1
    - fix B0014 bug
    - fix B0013 bug
    - add abnormal termination recovery routine
    - add ignore checksum option
    - fix B0012 bug
    - set SQLite lock timeout to 120s
    - improve scheduler (increase queue and dequeue performance)
    - frozen wget watchdog reactivation
Version 2.0 - 2012-02-14
    - add new synchronisation mode (retrieve dataset last version only)
    - fix B0011 bug (remove local files when checksum doesn't match)
    - add list-local-files action
    - fix B0007 bug (replace urllib with urllib2 and set timeout to 10)
    - fix B0006 bug (add missing env. var. in stop.sh)
    - fix B0009 bug (catch exception and process others datasets)
    - remove non-working models from models table
Version 1.9 - 2012-01-30
    - fix B0005 bug
Version 1.8 - 2012-01-28
    - add ``-w`` option (shutdown immediate)
    - improve errors handling
    - fix B0003 bug
    - fix start.sh ``-e`` option (B0004 bug)
Version 1.7 - 2012-01-27
    - add start.sh ``-u`` option (refresh ESGF metadata)
    - add start.sh ``-q`` option (stop daemon)
    - add start.sh ``-l`` option (list selections)
Version 1.6 - 2012-01-26
    - fix B0001 and B0002 bugs
    - remove one-file-per-model logging
    - add metadata caching system
    - merge all logs in one file
    - add model in tmp tables (dataset_version and file_timeslice)
Version 1.5 - 2012-01-18
    - move models loop inside the feeder
    - add CMOR tablename forcing in template
    - add stat subcommand
    - add syncmode check in start.sh
    - move product out of local_image column
Version 1.4 - 2012-01-14
    - set myproxy-logon as default (change procedure in README to use ``install.sh -a``)
    - add delete subcommand
    - add cancel subcommand
    - add retry subcommand
    - add info subcommand
    - merge output1 and output2 into output
    - improve installation process
    - use synchronous events to control the daemon
Version 1.3 - 2012-01-02
    - automatic update of model/datanode list
    - add remote and local checksum
    - unset X509_USER_PROXY variable (in get_data.sh script)
    - fix selection overlapping bug
    - fix product bug (check to prevent ``output`` value for product)
    - add license information
    - add svn properties in header
    - ignore blank lines in selection files
Version 1.2 - 2011-10-07
    - improve ``ensemble`` support
    - increase from 8 to 16 Wget threads
    - add per model priority
    - move main loop delay from 3 seconds to 6 seconds
    - support file ID with non-standard extension (``.nc_0``)
    - add upgrade and archive option in script install.sh
    - improve HTTP error handling in script get_data.sh
Version 1.1 - 2011-09-28
    - improve datanode and model configuration
    - improve HTTP error code handling
    - add watchdog to check for frozen wget
    - fix PCMDI datanode incorrect url
    - fix incorrect configuration for models GISS-E2-H, GISS-E2-R and inmcm4
    - add new models (HadCM3,IPSL-CM5A-LR,CanAM4,MIROC5,MIROC4h,CCSM4,MRI-CGCM3,MRI-AGCM3-2S,MRI-AGCM3-2H,MPI-ESM-LR)
Version 1.0 - 2011-09-09
    - support for ``myproxy-logon`` and ``myproxyclient``
    - simple data selection with model, experiment, realm and variable
    - multi threaded downloads (8 tasks by default)
    - manage datasets version following new drs
    - incremental process (download only what's new)
    - download history stored in a database

Post-Processing Module
**********************

Version 1.3 - 2017-01-15
    - *synda* group can be used instead of ``sudo`` (system package)
Version 1.2 - 2016-12-04
    - move hard-coded pipeline dependencies into configuration files
    - add ``credentials.conf`` file
    - add pipeline samples
    - bugfixes
Version 1.1 - 2016-09-19
    - add CORDEX support
    - add pexec support
    - add multivalues support for ``job_class`` option
    - add conf folder
    - add pipeline_path
    - improve worker log routines
Version 1.0 - 2014-12-25
    - pipeline engine
    - Jsonrpc server
    - database environment
    - worker script
