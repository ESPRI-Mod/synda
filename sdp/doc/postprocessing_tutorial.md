# Post-processing tutorial

## Synopsis

This documents contains instructions about how to trigger post-processing jobs once the download is complete.

## Requirements

Linux distribution with Python 2.6+.

## SDT module installation

SDT is the Synda module in charge of files transfer.

For this tutorial, SDT must be installed from source.

See instructions [here](https://github.com/Prodiguer/synda/blob/master/sdt/doc/src_install.md)

## SDP module installation

SDP is the Synda module in charge of files post-processing.

For this tutorial, SDP must be installed from source.

See instructions [here](https://github.com/Prodiguer/synda/blob/master/sdp/doc/src_install.md)

## Pipeline definition file creation

We will define a new pipeline called P001.

To do this, we must edit the file *P001.py*.

This file is located in ${SP_HOME}/conf/pipeline/P001.py

Edit this file so it looks like this:

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

## Binding file creation

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

## Job scripts creation

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

    $ synda daemon start

## Start SDP service

This is the server side post-processing daemon.

To start the service, run command below

    $ synda_pp daemon start

## Start SDW service

This is the client side post-processing daemon (aka 'worker').

To start the service, run command below

    $ synda_wo start

## Test communication between Synda modules

Test communication between SDW and SDP

    $ synda_wo -t -v

Test communication between SDT and SDP

    /usr/share/python/synda/sdt/bin/sdppproxy.py -v

It tests failed, check if credentials are correctly set in files below

    * $SP_HOME/conf/credentials.conf
    * $SP_HOME/bin/synda_wo
    * $ST_HOME/conf/credentials.conf

## Download files

Now the environment is ready, we can download some files.

    $ synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 baresoilFrac
