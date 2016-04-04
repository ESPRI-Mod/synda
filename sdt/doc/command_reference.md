# Command reference

## autoremove

Remove old datasets versions

usage: synda autoremove [-h] [-z]

optional arguments:
  -h, --help     show this help message and exit
  -z, --dry_run

## certificate

Manage X509 certificate

usage: synda certificate [-h] [-x] [{renew,print}]

positional arguments:
  {renew,print}         action

optional arguments:
  -h, --help            show this help message and exit
  -x, --force_renew_ca_certificates
                        Force renew CA certificates

examples
  synda certificate renew
  synda certificate print

## contact

Print contact information

usage: synda contact [-h]

optional arguments:
  -h, --help  show this help message and exit

## daemon

Daemon management

usage: synda daemon [-h] [{start,stop,status}]

positional arguments:
  {start,stop,status}  action

optional arguments:
  -h, --help           show this help message and exit

## dump

Display raw metadata

usage: synda dump [-h] [-s SELECTION_FILE] [-n] [-z] [-a | -d | -f | -v] [-A]
                  [-R] [-C COLUMN] [-F {raw,line,indent,value}]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

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
  synda dump CORDEX IPSL-INERIS  evaluation 1 -f -F indent
  synda dump CMIP5 IPSL mon atmos 1 -d -F indent
  synda dump -R CMIP5 1 -f -F indent
  synda dump omldamax_day_IPSL-CM5A-LR_decadal1995_r1i1p1_19960101-20051231.nc -F indent
  synda dump -R CMIP5 1 -f -F value -C url_http,url_gridftp
  synda dump CORDEX IPSL-INERIS  evaluation 1 -f -C local_path -F value

## facet

Facet discovery

usage: synda facet [-h] [-s SELECTION_FILE] [-n] [-z]
                   facet_name [parameter [parameter ...]]

positional arguments:
  facet_name            Facet name
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run

examples
  synda facet experiment MPI-ESM-LR | column
  synda facet variable MPI-ESM-LR | column
  synda facet experiment fddtalk MPI-ESM-LR

## help

Show help

usage: synda help [-h] [topic]

positional arguments:
  topic

optional arguments:
  -h, --help  show this help message and exit

## history

Show history

usage: synda history [-h]

optional arguments:
  -h, --help  show this help message and exit

## install

Install dataset

usage: synda install [-h] [-s SELECTION_FILE] [-n] [-z] [-y]
                     [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -y, --yes             assume "yes" as answer to all prompts and run non-interactively

## intro

Print introduction to synda command

usage: synda intro [-h]

optional arguments:
  -h, --help  show this help message and exit

## list

List installed dataset

usage: synda list [-h] [-s SELECTION_FILE] [-n] [-z] [-a | -d | -f | -v]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -a, --aggregation
  -d, --dataset
  -f, --file
  -v, --variable

examples
  synda list 5 -f
  synda list 5 -d

## metric

Display performance and disk usage metrics

usage: synda metric [-h] [--groupby {data_node,project,model}]
                    [--metric {rate,size}] [--project PROJECT]

optional arguments:
  -h, --help            show this help message and exit
  --groupby {data_node,project,model}, -g {data_node,project,model}
                        Group-by clause
  --metric {rate,size}, -m {rate,size}
                        Metric name
  --project PROJECT, -p PROJECT
                        Project name (must be used with '--groupby=model' else ignored)

examples
  synda metric -g data_node -m rate -p CMIP5
  synda metric -g project -m size

## param

Display ESGF parameters

usage: synda param [-h] [-c COLUMNS] [pattern1] [pattern2]

positional arguments:
  pattern1              Parameter name
  pattern2              Filter

optional arguments:
  -h, --help            show this help message and exit
  -c COLUMNS, --columns COLUMNS

examples
  synda param institute | column
  synda param institute NA
  synda param | column

## pexec

Execute post-processing task

usage: synda pexec [-h] [-s SELECTION_FILE] [-n] [-z] [-a | -d | -f | -v]
                   order_name

positional arguments:
  order_name            Order name

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -a, --aggregation
  -d, --dataset
  -f, --file
  -v, --variable

## queue

Display download queue status

usage: synda queue [-h] [project]

positional arguments:
  project     ESGF project (e.g. CMIP5)

optional arguments:
  -h, --help  show this help message and exit

examples
  synda queue obs4MIPs
  synda queue CMIP5
  synda queue

## remove

Remove dataset

usage: synda remove [-h] [-s SELECTION_FILE] [-n] [-z]
                    [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run

examples
  synda remove cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529
  synda remove CMIP5 MIROC-ESM historicalNat mon

## replica

Move to next replica

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

## reset

Remove all 'waiting' and 'error' transfers

usage: synda reset [-h]

optional arguments:
  -h, --help  show this help message and exit

## retry

Retry transfer (switch error status to waiting)

usage: synda retry [-h]

optional arguments:
  -h, --help  show this help message and exit

## search

Search dataset

usage: synda search [-h] [-s SELECTION_FILE] [-n] [-z] [-r]
                    [-a | -d | -f | -v]
                    [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -r, --replica         show replica
  -a, --aggregation
  -d, --dataset
  -f, --file
  -v, --variable

examples
  synda search experiment=rcp45,rcp85 model=CCSM4
  synda search project=ISI-MIP%20Fasttrack searchapi_host=esg.pik-potsdam.de
  synda search project=CMIP5 realm=atmos
  synda search realm=atmos project=CMIP5
  synda search atmos 50
  synda search MIROC rcp45 2
  synda search CCSM4 rcp45 atmos mon r1i1p1
  synda search title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc project=EUCLIPSE
  synda search title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc
  synda search clt_day_CanESM2_esmControl_r1i1p1_19010101-22501231.nc
  synda search pr_day_MPI-ESM-LR_abrupt4xCO2_r1i1p1_18500101-18591231.nc
  synda search c20c.UCT-CSAG.HadAM3P-N96.NonGHG-Hist.HadCM3-p50-est1.v1-0.mon.atmos.run060.v20140528
  synda search title=rlds_bced_1960_1999_gfdl-esm2m_rcp8p5_2051-2060.nc searchapi_host=esg.pik-potsdam.de
  synda search tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
  synda search tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613
  synda search dataset_id=tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
  synda search cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc

## selection

List selection files

usage: synda selection [-h]

optional arguments:
  -h, --help  show this help message and exit

## show

Display detailed information about dataset

usage: synda show [-h] [-s SELECTION_FILE] [-n] [-z] [-l] [--verbose]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run
  -l, --localsearch     search in local data repository (already installed dataset)
  --verbose             verbose mode

examples
  synda show cmip5.output1.CCCma.CanESM2.historicalGHG.fx.atmos.fx.r0i0p0.v20120410.orog_fx_CanESM2_historicalGHG_r0i0p0.nc
  synda show cmip5.output1.IPSL.IPSL-CM5A-LR.historical.mon.land.Lmon.r1i1p1.v20120430

## stat

Display summary information about dataset

usage: synda stat [-h] [-s SELECTION_FILE] [-n] [-z]
                  [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run

examples
  synda stat cmip5.output1.MOHC.HadGEM2-A.amip4xCO2.mon.atmos.Amon.r1i1p1.v20131108
  synda stat cmip5.output1.CCCma.CanCM4.decadal1964.mon.ocean.Omon.r1i1p1.v20120622
  synda stat MPI-ESM-LR rcp26

## test

Test file download

usage: synda test [-h] file_url

positional arguments:
  file_url    file url

optional arguments:
  -h, --help  show this help message and exit

examples
  synda test http://esgf1.dkrz.de/thredds/fileServer/cmip5/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/baresoilFrac/baresoilFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc
  synda test http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CCCma/CanESM2/esmFdbk2/mon/ocean/Omon/r1i1p1/zostoga/1/zostoga_Omon_CanESM2_esmFdbk2_r1i1p1_200601-210012.nc

## update

Update ESGF parameter local cache

usage: synda update [-h] [-i INDEX_HOST] [-p PROJECT]

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX_HOST, --index_host INDEX_HOST
                        Retrieve parameters from the specified index
  -p PROJECT, --project PROJECT
                        Retrieve project specific parameters for the specified project

## upgrade

Perform an upgrade (retrieve new version for all selection files)

usage: synda upgrade [-h] [-z] [-y] [parameter [parameter ...]]

positional arguments:
  parameter      search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help     show this help message and exit
  -z, --dry_run
  -y, --yes      assume "yes" as answer to all prompts and run non-interactively

## version

List all versions of a dataset

usage: synda version [-h] [-s SELECTION_FILE] [-n] [-z]
                     [parameter [parameter ...]]

positional arguments:
  parameter             search parameters. Format is name=value1,value2.. ... Most of the time, parameter name can be omitted.

optional arguments:
  -h, --help            show this help message and exit
  -s SELECTION_FILE, --selection_file SELECTION_FILE
  -n, --no_default      prevent loading default value
  -z, --dry_run

examples
  synda version cmip5.output1.MOHC.HadGEM2-A.amip4xCO2.mon.atmos.Amon.r1i1p1.v20131108
  synda version cmip5.output1.NCAR.CCSM4.rcp26.mon.atmos.Amon.r1i1p1.v20130426

## watch

Display running transfer

usage: synda watch [-h]

optional arguments:
  -h, --help  show this help message and exit

