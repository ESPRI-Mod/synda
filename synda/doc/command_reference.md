# *synda* command reference

## Synopsis

    synda SUBCOMMAND [args]

## Description

*synda* is the command-line client of Synda. Its functionality is offered via a
collection of task-specific subcommands, most of which accept a number of
options for fine-grained control of the program's behavior.

Available subcommands are:

    autoremove   Remove old datasets versions
    certificate  Manage X509 certificate
    check        Perform check over ESGF metadata
    contact      Print contact information
    count        Count dataset
    daemon       Daemon management
    dump         Display raw metadata
    facet        Facet discovery
    get          Download dataset
    help         Show help
    history      Show history
    install      Install dataset
    intro        Print introduction to synda command
    list         List installed dataset
    metric       Display performance and disk usage metrics
    open         Open netcdf file
    param        Print ESGF facets
    pexec        Execute post-processing task
    queue        Display download queue status
    remove       Remove dataset
    replica      Move to next replica
    reset        Remove all 'waiting' and 'error' transfers
    retry        Retry transfer (switch status from error to waiting)
    search       Search dataset
    selection    List selection files
    show         Display detailed information about dataset
    stat         Display summary information about dataset
    update       Update ESGF parameter local cache
    upgrade      Run 'install' command on all selection files
    variable     Print variable
    version      List all versions of a dataset
    watch        Display running transfer

Each subcommand is detailed in the next section.

## Subcommands description

### autoremove

Remove old datasets versions

```
usage: synda autoremove [-h] [-z]

optional arguments:
  -h, --help     show this help message and exit
  -z, --dry_run
```

### certificate

Manage X509 certificate

```
usage: synda certificate [-h] [-d] [-o OPENID] [-p PASSWORD] [-x]
                         [{renew,print}]

positional arguments:
  {renew,print}         action

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Display debug message
  -o OPENID, --openid OPENID
                        ESGF openid
  -p PASSWORD, --password PASSWORD
                        ESGF password
  -x, --force_renew_ca_certificates
                        Force renew CA certificates

examples
  synda certificate renew
  synda certificate print
```

### check

Perform check over ESGF metadata

```
usage: synda check [-h] [-s SELECTION_FILE] [-z] [-p FILE | -r FILE]
                   [-o {text,pdf}]
                   [{dataset_version,file_variable,selection}]
                   [parameter [parameter ...]]

positional arguments:
  {dataset_version,file_variable,selection}
                        action
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -z, --dry_run
  -p FILE, --playback FILE
                        Read metadata from FILE
  -r FILE, --record FILE
                        Write metadata to FILE
  -o {text,pdf}, --output_format {text,pdf}
                        Set output format

description
  dataset_version
    synda check dataset_version [search_parameter ...] checks the
    correctness and consistency of dataset version numbers in all dataset
    versions (or, if search parameters are given, those that match those
    parameters).

    The first check consists in verifying that version numbers are
    syntactically valid. The "version" field is deemed valid if it matches
    (case-insensitively) the Python regular expression /^(\d+)$/ or, as an
    extension, /^v(\d+)$/. A missing "version" field is the same as a
    "version" field set to "0".

    The second check only applies to datasets which have more than one
    version. It consists in verifying that all the versions of a dataset
    have unique version numbers. An integral version number is extracted
    from the value of each "version" field by converting the string
    matched by the capture group in the regular expressions above to an
    integer. For example, a "version" field set to "20160101" would match
    regexp /^(\d+)$/ therefore the version number would be 20160101. There
    must be no duplicated version numbers in all the versions of a
    dataset. Note that this test is more stringent than merely checking
    for duplicated "version" fields : a dataset with two versions having
    "version" fields set to "1" and "01" respectively would not pass
    because both have version number 1.

    If all the versions of a dataset have a "timestamp" field, a third
    check is done. The versions of a dataset are sorted by time stamp and
    the sequence numbers are examined. Gaps in the sequence are accepted
    but the numbers must be increasing. For example, this dataset would
    pass :

                           timestamp             version
                           2016-01-01T00:00:00Z  1
                           2016-01-02T00:00:00Z  20160102

    but this one would not :

                           timestamp             version
                           2016-01-01T00:00:00Z  20160101
                           2016-01-02T00:00:00Z  2

    By default, the report is in plain text format and is written to standard
    output. The pdf format can be used instead through the use of
    '--output_format' option.
    
    The report comprises four parts :

    - A header which gives the date and time of execution and the Synda
      command line.

    - For every dataset with errors, the name of the dataset and, for each
      of its versions, the "timestamp" and "version" fields along with a
      list of the errors found in this dataset version, if any.

    - Statistics :
      - the number of dataset versions found
      - ... with a "timestamp" field
      - ... without a "timestamp" field
      - the number of datasets found
      - ... with a "timestamp" field on all  of their versions
      - ... with a "timestamp" field on some of their versions
      - ... with a "timestamp" field on none of their versions

    - For each type of error,
      - a detailed description of the error,
      - the number of dataset versions in which it was found,
      - the number of datasets to which it applies, ie datasets with at
        least one version having in error.
  file_variable
    list files having more than one variable
  selection
    check if selection files parameters are valid

examples
  synda check dataset_version
  synda check file_variable CMIP5 atmos orog
  synda check selection
```

### contact

Print contact information

```
usage: synda contact [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### count

Count dataset

```
usage: synda count [-h] [-s SELECTION_FILE] [-n] [-z] [-i INDEX_HOST]
                   [-a | -d | -f | -v]
                   [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -i INDEX_HOST, --index_host INDEX_HOST
                        Retrieve parameters from the specified index
  -a, --aggregation
  -d, --dataset
  -f, --file
  -v, --variable

examples
  synda count
  synda count CMIP5
  synda count obs4MIPs -f
  synda count -s selection.txt --timestamp_left_boundary 2012-01-01T01:00:00Z --timestamp_right_boundary 2015-01-01T01:00:00Z
```

### daemon

Daemon management

```
usage: synda daemon [-h] [{start,stop,status}]

positional arguments:
  {start,stop,status}  action

optional arguments:
  -h, --help           show this help message and exit

notes
  This command is for source installation only (in system package
  installation, Synda daemon is installed as a service and is managed
  using 'service' command).
```

### dump

Display raw metadata

```
usage: synda dump [-h] [-s SELECTION_FILE] [-n] [-z] [-a | -d | -f | -v] [-A]
                  [-R] [-C COLUMN] [-F {raw,line,indent,value}]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -a, --aggregation
  -d, --dataset
  -f, --file
  -v, --variable
  -A, --all             Show all attributes
  -R, --raw_mode        dump original metadata
  -C COLUMN, --column COLUMN
                        set column(s) to be used with 'dump' action
  -F {raw,line,indent,value}, --format {raw,line,indent,value}
                        set format to be used with 'dump' action

examples
  synda dump CORDEX IPSL-INERIS  evaluation limit=1 -f -F indent
  synda dump CMIP5 IPSL mon atmos limit=1 -d -F indent
  synda dump -R CMIP5 limit=1 -f -F indent
  synda dump omldamax_day_IPSL-CM5A-LR_decadal1995_r1i1p1_19960101-20051231.nc -F indent
  synda dump -R CMIP5 limit=1 -f -F value -C url_http,url_gridftp
  synda dump CORDEX IPSL-INERIS  evaluation limit=1 -f -C local_path -F value
```

### facet

Facet discovery

```
usage: synda facet [-h] [-s SELECTION_FILE] [-z]
                   facet_name [parameter [parameter ...]]

positional arguments:
  facet_name            Facet name
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -z, --dry_run

examples
  synda facet experiment MPI-ESM-LR | column
  synda facet variable MPI-ESM-LR | column
  synda facet experiment fddtalk MPI-ESM-LR
```

### get

Download dataset

```
usage: synda get [-h] [-s SELECTION_FILE] [-z] [--verify_checksum]
                 [--dest_folder DEST_FOLDER] [--force]
                 [--network_bandwidth_test] [--openid OPENID]
                 [--password PASSWORD] [--quiet] [--timeout TIMEOUT]
                 [--urllib2] [--verbosity] [--hpss] [--no-hpss]
                 [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -z, --dry_run
  --verify_checksum, -c
                        Compare remote and local checksum
  --dest_folder DEST_FOLDER, -d DEST_FOLDER
                        Destination folder
  --force, -f           Overwrite local file if exists
  --network_bandwidth_test, -n
                        Prevent disk I/O to measure network throughput. When
                        this option is used, local file is set to /dev/null.
  --openid OPENID, -o OPENID
                        ESGF openid
  --password PASSWORD, -p PASSWORD
                        ESGF password
  --quiet, -q
  --timeout TIMEOUT, -t TIMEOUT
                        HTTP timeout
  --urllib2, -u         Use urllib2 instead of wget as HTTP client
  --verbosity, -v
  --hpss                Enable 'hpss' flag
  --no-hpss             Disable 'hpss' flag (Default)

examples
  synda get cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601
  synda get http://esgf1.dkrz.de/thredds/fileServer/cmip5/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc
  synda get sfcWind_ARC-44_ECMWF-ERAINT_evaluation_r1i1p1_AWI-HIRHAM5_v1_sem_197903-198011.nc
  synda get clcalipso_cfDay_NICAM-09_aqua4K_r1i1p1_00000101-00000330.nc
  synda get -d CORDEX 1
  synda get -f CMIP5 fx 1
  synda get protocol=gridftp limit=1 -f
  synda get uo_Omon_FGOALS-gl_past1000_r1i1p1_100001-199912.nc wmo_Omon_FGOALS-gl_past1000_r1i1p1_100001-199912.nc
  synda get http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CCCma/CanESM2/esmFdbk2/mon/ocean/Omon/r1i1p1/zostoga/1/zostoga_Omon_CanESM2_esmFdbk2_r1i1p1_200601-210012.nc
  synda get gsiftp://esgf1.dkrz.de:2811//cmip5/cmip5/output2/MPI-M/MPI-ESM-P/past1000/mon/ocean/Omon/r1i1p1/v20131203/umo/umo_Omon_MPI-ESM-P_past1000_r1i1p1_112001-112912.nc
  synda get http://esgf1.dkrz.de/thredds/fileServer/cmip5/cmip5/output2/MPI-M/MPI-ESM-P/past1000/mon/ocean/Omon/r1i1p1/v20131203/umo/umo_Omon_MPI-ESM-P_past1000_r1i1p1_112001-112912.nc
  synda get cmip5.output2.MPI-M.MPI-ESM-P.past1000.mon.ocean.Omon.r1i1p1.v20131203.rhopoto_Omon_MPI-ESM-P_past1000_r1i1p1_179001-179912.nc
```

### help

Show help

```
usage: synda help [-h] [topic]

positional arguments:
  topic

optional arguments:
  -h, --help  show this help message and exit
```

### history

Show history

```
usage: synda history [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### install

Install dataset

```
usage: synda install [-h] [-s SELECTION_FILE] [-n] [-z] [-y] [-i]
                     [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -y, --yes             assume "yes" as answer to all prompts and run non-
                        interactively
  -i, --incremental     Install files which appeared since last run
                        (experimental)

examples
  synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
  synda install sfcWind_ARC-44_ECMWF-ERAINT_evaluation_r1i1p1_AWI-HIRHAM5_v1_sem_197903-198011.nc
  synda install MPI-ESM-LR rcp26

notes
  'install' command is asynchronous, the transfer is handled by a
  background process. To check when the download is complete, use 'synda 
  queue' command.
```

### intro

Print introduction to synda command

```
usage: synda intro [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### list

List installed dataset

```
usage: synda list [-h] [-s SELECTION_FILE] [-z] [-a | -d | -f | -v]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -z, --dry_run
  -a, --aggregation
  -d, --dataset
  -f, --file
  -v, --variable

examples
  synda list limit=5 -f
  synda list limit=5 -d
```

### metric

Display performance and disk usage metrics

```
usage: synda metric [-h] [-z] [--groupby {data_node,project,model}]
                    [--metric {rate,size}] [--project PROJECT]

optional arguments:
  -h, --help            show this help message and exit
  -z, --dry_run
  --groupby {data_node,project,model}, -g {data_node,project,model}
                        Group-by clause
  --metric {rate,size}, -m {rate,size}
                        Metric name
  --project PROJECT, -p PROJECT
                        Project name (must be used with '--groupby=model' else
                        ignored)

examples
  synda metric -g data_node -m rate -p CMIP5
  synda metric -g project -m size
```

### open

Open netcdf file

```
usage: synda open [-h] [-s SELECTION_FILE] [-z] [--geometry GEOMETRY]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -z, --dry_run
  --geometry GEOMETRY, -g GEOMETRY
                        Window geometry

examples
  synda open cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc
  synda open -g 1000x600+70+0 orog_fx_CanESM2_historicalGHG_r0i0p0.nc
```

### param

Print ESGF facets

```
usage: synda param [-h] [-c COLUMNS] [pattern1] [pattern2]

positional arguments:
  pattern1              Parameter name
  pattern2              Filter

optional arguments:
  -h, --help            show this help message and exit
  -c COLUMNS, --columns COLUMNS

examples
  synda param | column
  synda param institute | column
  synda param institute NA
  synda param project
```

### pexec

Execute post-processing task

```
usage: synda pexec [-h] [-s SELECTION_FILE] [-n] [-z] {cdf}

positional arguments:
  {cdf}                 Order name

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
```

### queue

Display download queue status

```
usage: synda queue [-h] [project]

positional arguments:
  project     ESGF project (e.g. CMIP5)

optional arguments:
  -h, --help  show this help message and exit

examples
  synda queue obs4MIPs
  synda queue CMIP5
  synda queue
```

### remove

Remove dataset

```
usage: synda remove [-h] [-s SELECTION_FILE] [-n] [-z] [-y] [--verbose] [-m]
                    [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -y, --yes             assume "yes" as answer to all prompts and run non-
                        interactively
  --verbose             verbose mode
  -m, --keep_data       Remove only metadata

examples
  synda remove cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529
  synda remove status=error -n
  synda remove data_node=vesg.ipsl.upmc.fr,tds.ucar.edu,esgnode2.nci.org.au status=error -n
  synda remove CMIP5 MIROC-ESM historicalNat mon
```

### replica

Move to next replica

```
usage: synda replica [-h] [-z] [{next}] [file_id]

positional arguments:
  {next}         action
  file_id        File identifier (ESGF instance_id)

optional arguments:
  -h, --help     show this help message and exit
  -z, --dry_run

examples
  synda replica next
  synda replica next cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc
```

### reset

Remove all 'waiting' and 'error' transfers

```
usage: synda reset [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### retry

Retry transfer (switch status from error to waiting)

```
usage: synda retry [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### search

Search dataset

```
usage: synda search [-h] [-s SELECTION_FILE] [-n] [-z] [-l LIMIT] [-r]
                    [-a | -d | -f | -v]
                    [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -l LIMIT, --limit LIMIT
                        Set the total number of returned results. By default,
                        returns the first 100 records matching the given
                        constraints. Limit can be also be changed through the
                        keyword parameters limit=. The system imposes a
                        maximum value of limit <= 10,000.
  -r, --replica         show replica
  -a, --aggregation
  -d, --dataset
  -f, --file
  -v, --variable

examples
  synda search cmip5 output1 MOHC HadGEM2-A amip4xCO2 mon atmos Amon r1i1p1
  synda search rcp85 3hr timeslice=20050101-21001231 -f
  synda search project=CORDEX 'query=domain:EUR*11*'
  synda search rcp85 3hr start=2005-01-01T00:00:00Z end=2100-12-31T23:59:59Z -d
  synda search timeslice=00100101-20501231 model=GFDL-ESM2M "Air Temperature" -f
  synda search experiment=rcp45,rcp85 model=CCSM4
  synda search project=CMIP5 realm=atmos
  synda search realm=atmos project=CMIP5
  synda search CMIP5 frequency=day atmos tas -d
  synda search CMIP5 frequency=day atmos tas -v
  synda search CMIP5 frequency=day atmos tas -f
  synda search project=ISI-MIP%20Fast%20Track searchapi_host=esg.pik-potsdam.de
  synda search atmos 50
  synda search MIROC rcp45 2
  synda search CCSM4 rcp45 atmos mon r1i1p1
  synda search variable=tas institute!=MPI-M
  synda search title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc project=EUCLIPSE
  synda search title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc
  synda search clt_day_CanESM2_esmControl_r1i1p1_19010101-22501231.nc
  synda search pr_day_MPI-ESM-LR_abrupt4xCO2_r1i1p1_18500101-18591231.nc
  synda search c20c.UCT-CSAG.HadAM3P-N96.NonGHG-Hist.HadCM3-p50-est1.v1-0.mon.atmos.run060.v20140528
  synda search title=rlds_bced_1960_1999_gfdl-esm2m_rcp8p5_2051-2060.nc searchapi_host=esg.pik-potsdam.de
  synda search tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
  synda search tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613
  synda search dataset_id=tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
  synda search http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CCCma/CanESM2/esmFdbk2/mon/ocean/Omon/r1i1p1/zostoga/1/zostoga_Omon_CanESM2_esmFdbk2_r1i1p1_200601-210012.nc
  synda search gsiftp://esgf1.dkrz.de:2811//cmip5/cmip5/output2/MPI-M/MPI-ESM-P/past1000/mon/ocean/Omon/r1i1p1/v20131203/umo/umo_Omon_MPI-ESM-P_past1000_r1i1p1_112001-112912.nc
  synda search cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc
```

### selection

List selection files

```
usage: synda selection [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### show

Display detailed information about dataset

```
usage: synda show [-h] [-s SELECTION_FILE] [-n] [-z] [-l] [--verbose]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -l, --localsearch     search in local data repository (already installed
                        dataset)
  --verbose             verbose mode

examples
  synda show cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc
  synda show cmip5.output1.IPSL.IPSL-CM5A-LR.historical.mon.land.Lmon.r1i1p1.v20120430
```

### stat

Display summary information about dataset

```
usage: synda stat [-h] [-s SELECTION_FILE] [-n] [-z] [-i]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -i, --incremental     Limit action on files which appeared since last run
                        (experimental)

examples
  synda stat cmip5.output1.MOHC.HadGEM2-A.amip4xCO2.mon.atmos.Amon.r1i1p1.v20131108
  synda stat cmip5.output1.CCCma.CanCM4.decadal1964.mon.ocean.Omon.r1i1p1.v20120622
  synda stat MPI-ESM-LR rcp26
  synda stat project=CORDEX 'query=domain:EUR*11*'
  synda stat ECMWF-ERAINT frequency=day
```

### update

Update ESGF parameter local cache

```
usage: synda update [-h] [-i INDEX_HOST] [-p PROJECT]

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX_HOST, --index_host INDEX_HOST
                        Retrieve parameters from the specified index
  -p PROJECT, --project PROJECT
                        Retrieve project specific parameters for the specified
                        project
```

### upgrade

Run 'install' command on all selection files

```
usage: synda upgrade [-h] [-z] [-y] [-i] [-e FILE] [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -z, --dry_run
  -y, --yes             assume "yes" as answer to all prompts and run non-
                        interactively
  -i, --incremental     Install files which appeared since last run
                        (experimental)
  -e FILE, --exclude_from FILE
                        Read exclude selection-file from FILE
```

### variable

Print variable

```
usage: synda variable [-h] [-z] [-l] [-s] [-S] [parameter [parameter ...]]

positional arguments:
  parameter            search parameters. Format is name=value1,value2.. ...
                       Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help           show this help message and exit
  -z, --dry_run
  -l, --long_name
  -s, --short_name
  -S, --standard_name

examples
  synda variable
  synda variable -S
  synda variable -s
  synda variable sfcWind
  synda variable wind_speed
  synda variable Near-Surface Wind Speed
  synda variable Dissolved Inorganic Carbon Concentration
  synda variable cell_area
  export COLUMNS ; synda variable -s | cut -c 1-20 | column | less
```

### version

List all versions of a dataset

```
usage: synda version [-h] [-s SELECTION_FILE] [-n] [-z]
                     [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ...
                        Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run

examples
  synda version cmip5.output1.MOHC.HadGEM2-A.amip4xCO2.mon.atmos.Amon.r1i1p1.v20131108
  synda version cmip5.output1.NCAR.CCSM4.rcp26.mon.atmos.Amon.r1i1p1.v20130426
```

### watch

Display running transfer

```
usage: synda watch [-h]

optional arguments:
  -h, --help  show this help message and exit
```

