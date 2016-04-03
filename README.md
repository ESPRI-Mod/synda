# *synda*

## Synopsis

*Synda* is a command line tool to search and download files from the Earth
System Grid Federation (ESGF) archive.

The user defines one or many templates. Each of them have a list of
facets (variables, frequencies, experiments, ensemble, model..). Using
these templates, the program explore the ESGF archive and dowload all
the corresponding available files. The program may be run regularly to
download the possible new files. Typically each template is associated
with an analysis (cfmip template, downscaling template and so on).
Create as many template_name.txt as you want in the 'selection' folder.
Template file examples are given in the 'selection/sample' sub-folder. 

## Documentation

[Installation guide](#installation)                                   | [Upgrade guide](sdt/doc/upgrade_guide.md)

[User guide](sdt/doc/user_guide.md)                                   | [Admin guide](sdt/doc/admin_guide.md)

[Configuration parameter reference](sdt/doc/sdt_conf.md)

[Wiki](https://forge.ipsl.jussieu.fr/prodiguer/wiki/docs/synda)       | [Howto & Tutorial](sdt/doc/howto_and_tutorial.md)

[Faq](sdt/doc/faq.md)                                                 |[Template sample](sdt/doc/TEMPLATE)    |
[Changelog](sdt/doc/changelog)                                        |[License](sdt/doc/LICENSE)             |
[Slides](sdt/doc/synda.odp)

## Basic usage

Search datasets

    synda search FACET

Install a dataset

    synda install DATASET

## Motivation

This program is a command-line alternative to the ESGF web front-end.

## Main features

* Simple data installation using an apt-get like command
* Parallel downloads
* Incremental process (download only what's new)
* Download history stored in a db
* Transfer priority

## Platform

* Linux

## Version

* Stable: 3.2

* Testing: 3.3

## Dependency

* Python 2.6+

## Installation

[RPM installation](sdt/doc/rpm_install.md)

[DEB installation](sdt/doc/deb_install.md)

[Source installation](sdt/doc/src_install.md)

[Docker installation](https://registry.hub.docker.com/u/prodiguer/synda)

Notes:

* installations using system packages (DEB or RPM) are multi-user, and can
  only be performed by root user. Source installation is single-user and can be
  performed by root or normal user.
* installation guides for old Synda versions can be found [here](sdt/doc/old_version_installation_guide)

## Contact

sdipsl AT ipsl DOT jussieu DOT fr

## Acknowledgment

*synda* has incorporated code from several sources. Users have contributed
patches and suggestions over time. This work has been undertaken by IPSL and
as been funded by IPSL, IS-ENES and France-Grilles.
