# *synda*

## Program description

This program can download files from the Earth System Grid Federation
(ESGF) archive in an easy way, for a list of variables, experiments and
ensemble members. The program will evolve together with the ESGF
archive backend functionalities.

The user defines one or many templates. Each of them have a list of
facets (variables, frequencies, experiments, ensemble, model..). Using
these templates, the program explore the ESGF archive and dowload all
the corresponding available files. The program may be run regularly to
download the possible new files. Typically each template is associated
with an analysis (cfmip template, downscaling template and so on).
Create as many template_name.txt as you want in the 'selection'
folder. Selection examples are given in the 'sample' sub-folder. 

## Main features

* simple data installation using an apt-get like command
* parallel downloads
* incremental process (download only what's new)
* download history stored in a db
* transfer priority

## Last version

3.0

## Installation

As root, you need to install the following system package:

Centos

    yum install gcc python python-pip python-devel openssl-devel sqlite-devel libxslt-devel libxml2-devel zlib-devel libffi-devel


Debian

    apt-get install gcc python python-pip python-dev libssl-dev libsqlite-dev libxslt-dev libxml2-dev libz-dev libffi-dev

Then install the application as simple user or root:

    wget http://dods.ipsl.jussieu.fr/jripsl/synda/install.sh
    chmod +x ./install.sh
    ./install.sh

## Configuration

Add lines below in your shell configuration file (e.g. '.bashrc')

    export ST_HOME=$HOME/sdt
    export PATH=$ST_HOME/bin:$PATH

Then edit $ST_HOME/sdt.conf to set openid and password (ESGF credential).

Note: to download file from ESGF, you need to create an openID account on one
ESGF identity provider website (e.g. PCMDI, BADC or DKRZ) and subscribe to
CMIP5-RESEARCH role.

## Basic usage

Search datasets

    synda search FACET..

Install a dataset

    synda install DATASET..

Start the download

    synda daemon start

Check download completion

    synda queue status

Stop the download

    synda daemon stop

Downloaded files location

    $HOME/sdt/data

## User guide

http://dods.ipsl.jussieu.fr/jripsl/synda/user_guide.html

## Admin guide

http://dods.ipsl.jussieu.fr/jripsl/synda/admin_guide.html

## Upgrade guide

http://dods.ipsl.jussieu.fr/jripsl/synda/upgrade_guide.html

## Selection file sample

http://dods.ipsl.jussieu.fr/jripsl/synda/TEMPLATE

## Faq

http://dods.ipsl.jussieu.fr/jripsl/synda/FAQ

## License 

http://dods.ipsl.jussieu.fr/jripsl/synda/LICENSE

## Contact

<sdipsl AT ipsl DOT jussieu DOT fr>

## Acknowledgment

*synda* has incorporated code from several sources. Users have contributed
patches and suggestions over time. This work has been undertaken by IPSL and
as been funded by IPSL, IS-ENES and France-Grilles.
