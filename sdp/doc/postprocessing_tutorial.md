# Postprocessing tutorial

## Synopsis

This documents contains instructions about how to trigger postprocessing jobs once the download is complete.

## Requirements

Linux distribution with Python 2.6+.

## SDT module installation

See instructions [here](https://github.com/Prodiguer/synda#installation)

## SDP module installation

See instructions [here](https://github.com/Prodiguer/synda/blob/master/sdp/doc/src_install.md)

## Bindings file creation

The binding file is used to bind event to pipeline.

This file is located in pipeline/spbindings.py

For this tutorial, this file must configured as below

    import spconst

    event_pipeline_mapping={
        spconst.EVENT_VARIABLE_COMPLETE: ('P001', spconst.PPPRUN_STATUS_WAITING)
    }

    trigger={}

## Pipeline definition file creation

We now have to define a new pipeline called P001.

To do this, we must edit the file *P001.py*.

This file is located in pipeline/spbindings.py

Edit this file so it looks like 

    import sppipelineutils
    import sppostprocessingutils

    def get_pipeline():
        return ppp

    # init.

    name='P001'

    tasks=['task1','task2','task3']

    ppp=sppostprocessingutils.build_light_pipeline(name,tasks)

## Job scripts creation

FIXME

## Start SDT service

FIXME

## Start SDP service

FIXME

## Start SDW service

FIXME

## Download files

Now the environment is ready, we can download some files.
