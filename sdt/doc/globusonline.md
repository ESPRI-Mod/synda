# Globus Online Howto

## Requirement

Synda must be installed from source to transfer files with Globus Online
(not available yet with system package based installation).

## Installation

To install globusonline module in an already existing synda installation, do

    ./install.sh globusonline

To install a new installation of synda and globusonline, do

    ./install.sh synda globusonline

## Configuration

Synda Configuration Files

sdt/lib/sd/sdconfig.py:

    #download_manager='default' # default | globus_online                                                              
    download_manager='globus_online'

sdt/conf/credentials.conf:

    [globus]
    username=
    password=

sdt/conf/sdt.conf:

    [globus]
    destination_endpoint = destination#endpoint
    esgf_endpoints = /esg/config/esgf_endpoints.xml

ESGF Configuration Files

    /esg/config/esgf_endpoints.xml:

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <endpoints xmlns="http://www.esgf.org/whitelist">
        <endpoint
            name="cedaesgf#esgf-data1"
            gridftp="esgf-data1.ceda.ac.uk:2811"
            path_out="/"
            path_in=”/”
        />
        <endpoint
        name="esganl#7c3cf794-d9a4-11e5-ac97-22000b460624"
            gridftp="esg.anl.gov:2811"
            path_out="/"
            path_in=”/”
        />
        <endpoint
            name="esganl#5a43068a-d669-11e5-9765-22000b9da45e"
            gridftp="app006.cels.anl.gov:2811"
            path_out="/"
            path_in=”/”
        />
    </endpoints>
