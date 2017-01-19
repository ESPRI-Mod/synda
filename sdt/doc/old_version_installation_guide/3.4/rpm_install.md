# Synda RPM package installation guide

## Synopsis

This documents contains instructions to install Synda from RPM package.

## Requirements

*synda* RPM package is available for RHEL6 and RHEL7.

On RHEL5, Synda can only be installed from source.

## Installation

EPEL repository must be installed.

To install EPEL, use

```
sudo yum install epel-release -y
```

To install synda RPM package, use

```
wget http://sd-104052.dedibox.fr/synda/sdt/rpm/<package-name>
sudo yum install -y <package-name>
```

where &lt;package-name&gt; can be one of

* synda-3.4-1.x86_64_centos65.rpm
* synda-3.4-1.x86_64_centos67.rpm
* synda-3.4-1.x86_64_centos71.rpm
* synda-3.4-1.x86_64_fedora20.rpm
* synda-3.4-1.x86_64_fedora21.rpm
* synda-3.4-1.x86_64_fedora22.rpm
* synda-3.4-1.x86_64_fedora23.rpm
* synda-3.4-1.x86_64_scientific61.rpm
* synda-3.4-1.x86_64_scientific67.rpm
* synda-3.4-1.x86_64_scientific71.rpm

Example

To install Synda on Scientific Linux 6.7, do

```
sudo yum install http://sd-104052.dedibox.fr/synda/sdt/rpm/synda-3.4-1.x86_64_scientific67.rpm 
```

If you need a distro/version that is not listed, you can open a github issue so we can add it to the list.

Note: RPM packages are currently only available for 64 bits architecture

## Patch

Synda 3.4 RPM package contains a bug which prevent displaying error messages under certain circumstances.

Run the command below to fix it

```
sudo sed -i -e "s/install/get','install/" /usr/share/python/synda/sdt/bin/sdconst.py
```

## Configuration

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

* /etc/synda/sdt
* /srv/synda/sdt/data
* /srv/synda/sdt/sandbox
* /var/lib/synda/sdt
* /var/tmp/synda/sdt
* /var/tmp/synda/sdt/.esg/certificates
* /var/log/synda/sdt
* /usr/bin/synda
* /usr/share/python/synda/sdt
* /usr/share/doc/synda/sdt
