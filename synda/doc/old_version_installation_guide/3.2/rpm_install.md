# Synda 3.2 RPM package installation guide

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
sudo yum install http://sd-104052.dedibox.fr/synda/rpm/<package-name> -y
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
sudo yum install http://sd-104052.dedibox.fr/synda/rpm/synda-3.2-1.x86_64_scientific67.rpm 
```

If you need a distro/version that is not listed, you can open a github issue so we can add it to the list.

Note: RPM packages are currently only available for 64 bits architecture

## Patches

### Patch 1

Synda 3.2 RPM package contains a bug which prevent renewing certificate.

Run the command below to fix it

```
sudo /usr/share/python/synda/sdt/bin/pip install setuptools==1.0
```

### Patch 2

Synda 3.2 RPM package contains a bug which prevent running application under certain circumstances.

Run the command below to fix it

```
sudo wget http://sd-104052.dedibox.fr/synda/patches/3.2/sdcleanup_tree.sh -O /usr/share/python/synda/sdt/bin/sdcleanup_tree.sh
```

## Configuration

* Fix the ESGF index hostname

```
sudo vi /etc/synda/sdt/sdt.conf
```

Replace

```
indexes=pcmdi9.llnl.gov
default_index=pcmdi9.llnl.gov
```

with

```
indexes=pcmdi.llnl.gov
default_index=pcmdi.llnl.gov
```

* Edit credentials file to set ESGF openid and password

```
sudo vi /etc/synda/sdt/credentials.conf
```

Note: to download file from ESGF, you need to create an openID account on one
ESGF identity provider website (e.g. PCMDI, BADC, DKRZ..) and subscribe to
CMIP5-RESEARCH role.

* Restart service with

```
sudo service synda restart
```

## Usage

A quickstart guide is available by running 'intro' subcommand

```
synda intro | more
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
