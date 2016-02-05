# Synda installation using RPM package

## Synopsis

This documents contains instructions to install Synda from RPM package.

## Requirements

Synda RPM packages are available for RHEL6 and RHEL7.

On RHEL5, Synda can only be installed from source.

## Installation

EPEL repository must be installed.

To install EPEL, use

```
sudo yum install epel-release -y
```

To install synda RPM package, use

```
sudo yum install http://dods.ipsl.jussieu.fr/jripsl/synda/rpm/<package-name> -y
```

where &lt;package-name&gt; can be one of

* synda-3.2-1.x86_64_centos65.rpm
* synda-3.2-1.x86_64_centos67.rpm
* synda-3.2-1.x86_64_centos71.rpm
* synda-3.2-1.x86_64_fedora20.rpm
* synda-3.2-1.x86_64_fedora21.rpm
* synda-3.2-1.x86_64_fedora22.rpm
* synda-3.2-1.x86_64_fedora23.rpm
* synda-3.2-1.x86_64_scientific61.rpm
* synda-3.2-1.x86_64_scientific67.rpm
* synda-3.2-1.x86_64_scientific71.rpm

Example

To install Synda on Scientific Linux 6.7, do

```
sudo yum install http://dods.ipsl.jussieu.fr/jripsl/synda/rpm/synda-3.2-1.x86_64_scientific67.rpm 
```

If you need a distro/version that is not listed, you can open a github issue so we can add it to the list.

Note: RPM package are currently only available for 64 bits architecture

## Configuration

Edit credentials file to set ESGF openid and password

```
vi /etc/synda/sdt/credentials.conf
```

Note: to download file from ESGF, you need to create an openID account on one
ESGF identity provider website (e.g. PCMDI, BADC, DKRZ..) and subscribe to
CMIP5-RESEARCH role.

## Usage

A quickstart guide is available by running 'intro' subcommand

```
synda intro 
```

## Files location

Installing Synda from RPM package is multi-user (for single-user installation,
see 'installation from source' method)

* /etc/synda/sdt
* /srv/synda/sdt
* /var/lib/synda/sdt
* /var/tmp/synda/sdt
* /var/tmp/synda/sdt/.esg/certificates
* /var/log/synda/sdt
* /usr/bin/synda
* /usr/share/python/synda/sdt
* /usr/share/doc/synda/sdt
