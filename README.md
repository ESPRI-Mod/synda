# *synda*

## Synopsis

*Synda* is a command line tool to search and download files from the Earth
System Grid Federation (ESGF) archive.

The user defines one or many templates (aka selection file). Each of them have
a list of facets (variables, frequencies, experiments, ensemble, model..).
Using these templates, the program explore the ESGF archive and download all
the corresponding available files. The program may be run regularly to download
the possible new files. Typically each template is associated with an analysis
(cfmip template, downscaling template and so on). Create as many
template_name.txt as you want in the 'selection' folder.

## Usage

Search datasets

    synda search FACET

Install a dataset

    synda install DATASET

## Documentation

[Overview](sdt/doc/overview.md)                                       | [Faq](sdt/doc/faq.md)

[Installation guide](#installation)                                   | [Upgrade guide](sdt/doc/upgrade_guide.md)

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

* Installations using system packages (DEB or RPM) are multi-user, and can
  only be performed by root user. Source installation is single-user and can be
  performed by root or normal user.
* Installation guides for old Synda versions can be found [here](sdt/doc/old_version_installation_guide)

## Contact

sdipsl AT ipsl DOT jussieu DOT fr

## Acknowledgment

*synda* has incorporated code from several sources. Users have contributed
patches and suggestions over time. This work has been undertaken by IPSL and
as been funded by IPSL, IS-ENES and France-Grilles.
