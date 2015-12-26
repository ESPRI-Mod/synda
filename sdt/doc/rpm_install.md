
# Synda installation using RPM package

## Synopsis

This documents contains instructions to install Synda from RPM package.

## Installation

EPEL must be installed

To install EPEL on Centos 7, do

```
sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y
```

To install synda RPM package, use

```
sudo yum install http://dods.ipsl.jussieu.fr/jripsl/synda/rpm/<package-name> -y
```

where <package-name> can be one of

synda-3.1-1.x86_64_centos65.rpm
synda-3.1-1.x86_64_centos67.rpm
synda-3.1-1.x86_64_centos71.rpm
synda-3.1-1.x86_64_fedora20.rpm
synda-3.1-1.x86_64_fedora21.rpm
synda-3.1-1.x86_64_fedora22.rpm
synda-3.1-1.x86_64_fedora23.rpm
synda-3.1-1.x86_64_scientific61.rpm
synda-3.1-1.x86_64_scientific67.rpm
synda-3.1-1.x86_64_scientific71.rpm

## Configuration

Edit credentials file to set ESGF openid and password

```
vi /etc/synda/sdt/credentials.conf
```

Note: to download file from ESGF, you need to create an openID account on one
ESGF identity provider website (e.g. PCMDI, BADC or DKRZ) and subscribe to
CMIP5-RESEARCH role.
