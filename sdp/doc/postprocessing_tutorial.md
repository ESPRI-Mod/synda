# Post-processing tutorial

## Synopsis

This documents contains instructions about how to trigger post-processing jobs once the download is complete.

## Requirements

Linux distribution with Python 2.6+.

## SDT module installation

SDT is the Synda module in charge of files transfer.

For this tutorial, SDT must be installed from source and SDT version must be greater or equal to 3.7.

See instructions [here](https://github.com/Prodiguer/synda/blob/master/sdt/doc/src_install.md)

## SDP module installation

SDP is the Synda module in charge of files post-processing.

For this tutorial, SDP must be installed from source and SDP version must be greater or equal to 1.3.

See instructions [here](https://github.com/Prodiguer/synda/blob/master/sdp/doc/src_install.md)

## Configuration

### SDT module

Set 'post_processing' parameter to true in $ST_HOME/conf/sdt.conf

    post_processing=true

### SDP module

#### Pipeline definition file creation

We will define a pipeline called P001.

Edit the file below:

    ${SP_HOME}/conf/pipeline/P001.py

This file content must be:

    import sppipelineutils
    import sppostprocessingutils

    def get_pipeline():
        return ppp

    # init.

    name='P001'

    tasks=['foo','bar','foobar']

    ppp=sppostprocessingutils.build_light_pipeline(name,tasks)

This code basically means that P001 pipeline is composed of three tasks (foo,
bar and foobar), which will run sequentially one after the other.

#### Binding file creation

The binding file is used to bind events to pipelines.

This file is located in ${SP_HOME}/conf/pipeline/spbindings.py

For this tutorial, this file content must be

    import spconst

    event_pipeline_mapping={
        spconst.EVENT_FILE_COMPLETE: ('P001', spconst.PPPRUN_STATUS_WAITING)
    }

    trigger={}

This code binds the EVENT_FILE_COMPLETE event to P001 pipeline, and set the
initial pipeline status to 'waiting'.

#### Job scripts creation

We first create a directory to store the scripts.

    mkdir /tmp/synda_pp_scripts

We then create the three scripts corresponding to three pipeline tasks
that have been defined.

    cd /tmp/synda_pp_scripts
    wget -O foobar.sh https://raw.githubusercontent.com/Prodiguer/synda/master/sdw/script/template.sh
    chmod +x foobar.sh
    cp foobar.sh foo.sh
    cp foobar.sh bar.sh

## Start SDT service

This is the files transfer service.

To start the service, run command below

    synda daemon start

## Start SDP service

This is the server side post-processing daemon.

To start the service, run command below

    synda_pp daemon start

## Start SDW service

This is the client side post-processing daemon (aka 'worker').

To start the service, run command below

    synda_wo --script_dir /tmp/synda_pp_scripts start

## Test communication between Synda modules

Test communication between SDW and SDP

    synda_wo -t -v

Test communication between SDT and SDP

    $ST_HOME/lib/sd/sdppproxy.py -v

It tests failed, check if credentials are correctly set in files below then
restart the three daemons.

* $SP_HOME/conf/credentials.conf
* $SP_HOME/bin/synda_wo
* $ST_HOME/conf/credentials.conf

## Download files

Let's download a file

    synda install -y sfcWind_ARC-44_MPI-M-MPI-ESM-LR_historical_r1i1p1_SMHI-RCA4-SN_v1_sem_197012-198011.nc

After a few minutes, the file should have been transferred and the jobs should have been triggered.

To check the result, let's see the logfile

    vi $SP_HOME/log/worker.log

If all went well, the logfile should look like this

    2017/01/10 09:09:56 AM INFO Processing job (transition=foo,args={u'pipeline': u'P001', u'data_folder': u'/home/jerome/sdp/data', u'project': u'CORDEX', u'variable': u's
    fcWind', u'model': u'RCA4-SN', u'dataset_pattern': u'cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123'},job_class=foo,start_date=2017-01-10 09:09:56.791281,ppprun_id=1,error_msg=None)
    2017/01/10 09:09:56 AM DEBUG Script return code: 0
    2017/01/10 09:09:56 AM DEBUG Script stdout:  
    2017/01/10 09:09:56 AM DEBUG Script stderr: 
    2017-01-10 09:09:56 - INF001 - foo.sh script started
    2017-01-10 09:09:56 - INF002 - dataset_pattern: cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123
    2017-01-10 09:09:56 - INF003 - foo.sh script ends.
    2017/01/10 09:09:56 AM INFO Processing job (transition=bar,args={u'pipeline': u'P001', u'data_folder': u'/home/jerome/sdp/data', u'project': u'CORDEX', u'variable': u'sfcWind', u'model': u'RCA4-SN', u'dataset_pattern': u'cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123'},job_class=bar,start_date=2017-01-10 09:09:56.887659,ppprun_id=1,error_msg=None)
    2017/01/10 09:09:56 AM DEBUG Script return code: 0
    2017/01/10 09:09:56 AM DEBUG Script stdout:  
    2017/01/10 09:09:56 AM DEBUG Script stderr: 
    2017-01-10 09:09:56 - INF001 - bar.sh script started
    2017-01-10 09:09:56 - INF002 - dataset_pattern: cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123
    2017-01-10 09:09:56 - INF003 - bar.sh script ends.
    2017/01/10 09:09:57 AM INFO Processing job (transition=foobar,args={u'pipeline': u'P001', u'data_folder': u'/home/jerome/sdp/data', u'project': u'CORDEX', u'variable': u'sfcWind', u'model': u'RCA4-SN', u'dataset_pattern': u'cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123'},job_class=foobar,start_date=2017-01-10 09:09:56.985872,ppprun_id=1,error_msg=None)
    2017/01/10 09:09:57 AM DEBUG Script return code: 0
    2017/01/10 09:09:57 AM DEBUG Script stdout: 
    2017/01/10 09:09:57 AM DEBUG Script stderr: 
    2017-01-10 09:09:57 - INF001 - foobar.sh script started
    2017-01-10 09:09:57 - INF002 - dataset_pattern: cordex/output/ARC-44/SMHI/MPI-M-MPI-ESM-LR/historical/r1i1p1/RCA4-SN/v1/sem/sfcWind/v20140123
    2017-01-10 09:09:57 - INF003 - foobar.sh script ends.
