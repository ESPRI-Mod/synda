
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
sudo yum install http://dods.ipsl.jussieu.fr/jripsl/synda/rpm/rhel7/ -y
```

## Configuration

Edit credentials file to set ESGF openid and password

```
vi /etc/synda/sdt/credentials.conf
```

Note: to download file from ESGF, you need to create an openID account on one
ESGF identity provider website (e.g. PCMDI, BADC or DKRZ) and subscribe to
CMIP5-RESEARCH role.
