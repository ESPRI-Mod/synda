# *synda*

## Synopsis

*Synda* is a command line tool to search and download files from the Earth
System Grid Federation (ESGF) archive.

## Usage

Search dataset

    synda search cmip5 MOHC HadGEM2-A amip4xCO2 mon atmos Amon r1i1p1

    synda search rcp85 3hr start=2005-01-01T00:00:00Z end=2100-12-31T23:59:59Z

    synda search cmip5 mon atmos -l 1000

Search file

    synda search rcp85 3hr timeslice=20050101-21001231 -f

    synda search timeslice=00100101-20501231 model=GFDL-ESM2M "Air Temperature" -f

Download file

    synda get tasmax_day_FGOALS-s2_piControl_r1i1p1_20160101-20161231.nc

Manage a large number of files with install / remove

    synda install CMIP5 CNRM-CM5 tas pr areacello

    synda remove areacello

Explore metadata

    synda dump tas GFDL-ESM2M -F line -f -C size,filename 

    synda variable | less

    synda variable wind_speed_of_gust

    export COLUMNS ; synda variable -s | cut -c 1-20 | column | less

## Documentation

[Overview](sdt/doc/overview.md)                                       | [Faq](sdt/doc/faq.md)

[Installation Guide](#installation)                                   | [Upgrade guide](sdt/doc/upgrade_guide.md)

[User Guide](sdt/doc/user_guide.md)

[Command Reference](sdt/doc/command_reference.md)

[Configuration Parameter Reference](sdt/doc/configuration_parameter_reference.md)

[Selection File](sdt/doc/selection_file.md)                           | [Selection File Parameter Reference](sdt/doc/selection_file_parameter_reference.md) | [Selection File Example](https://github.com/Prodiguer/synda/tree/master/sdt/selection/sample)

[Howto & Tutorial](sdt/doc/howto_and_tutorial.md)

[Project](sdt/doc/project.md)

## Motivation

This program is a command-line alternative to the ESGF web front-end.

## Platform

* Linux

## Version

* Stable: 3.4

* Testing: 3.5

## Dependency

* Python 2.6+

## Installation

[RPM installation](sdt/doc/rpm_install.md)

[DEB installation](sdt/doc/deb_install.md)

[Source installation](sdt/doc/src_install.md)

[Docker installation](https://hub.docker.com/r/prodiguer/synda)

Notes:

* Source installation can be performed by root or normal user.
* When using system package installation, many *synda* commands cannot be executed by normal user (e.g. sudo must be used to execute "synda get" command).
* Installation guides for old *synda* versions can be found [here](sdt/doc/old_version_installation_guide)

## Contact

sdipsl AT ipsl DOT jussieu DOT fr

## Acknowledgment

*synda* has incorporated code from several sources. Users have contributed
patches and suggestions over time. This work has been undertaken by IPSL and
as been funded by IPSL, IS-ENES and France-Grilles.
