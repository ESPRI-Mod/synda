# *synda*

## Synopsis

*Synda* is a command line tool to search and download files from the Earth
System Grid Federation (ESGF) archive.

## Usage

Search file

    synda search 20160101-20161231 "Air Temperature" -f

Download file

    synda get tasmax_day_FGOALS-s2_piControl_r1i1p1_20160101-20161231.nc

Manage a large number of files with install / remove commands

    synda install CMIP5 CNRM-CM5 tas pr areacello

    synda remove areacello

## Documentation

[Overview](sdt/doc/overview.md)                                       | [Faq](sdt/doc/faq.md)

[Installation guide](#installation)                                   | [Upgrade guide](sdt/doc/upgrade_guide.md)

[Download Guide](download_guide.md)

[Command reference](sdt/doc/command_reference.md)

[Configuration parameter reference](sdt/doc/configuration_parameter_reference.md)

[Selection file](sdt/doc/selection_file.md)                           | [Selection file parameter reference](sdt/doc/selection_file_parameter_reference.md) | [Selection file example](https://github.com/Prodiguer/synda/tree/master/sdt/selection/sample)

[Howto & Tutorial](sdt/doc/howto_and_tutorial.md)

[Project](sdt/doc/project.md)

## Motivation

This program is a command-line alternative to the ESGF web front-end.

## Platform

* Linux

## Version

* Stable: 3.3

* Testing: 3.4

## Dependency

* Python 2.6+

## Installation

[RPM installation](sdt/doc/rpm_install.md)

[DEB installation](sdt/doc/deb_install.md)

[Source installation](sdt/doc/src_install.md)

[Docker installation](https://hub.docker.com/r/prodiguer/synda)

Notes:

* Source installation can be performed by root or normal user.
* Installation guides for old Synda versions can be found [here](sdt/doc/old_version_installation_guide)

## Contact

sdipsl AT ipsl DOT jussieu DOT fr

## Acknowledgment

*synda* has incorporated code from several sources. Users have contributed
patches and suggestions over time. This work has been undertaken by IPSL and
as been funded by IPSL, IS-ENES and France-Grilles.
