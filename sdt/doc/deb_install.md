# Synda installation using DEB package

## Synopsis

This documents contains instructions to install Synda from DEB package.

## Requirements

Synda DEB packages are available for Debian, Ubuntu and Mint.

## Installation

Add IPSL Synda repository to /etc/apt/sources.list

```
deb http://dods.ipsl.jussieu.fr/jripsl/synda/deb/repo/<distro-name>/ ipslrepo contrib
```

where &lt;distro-name&gt; can be one of

* ubuntu14
* ubuntu12
* mint17
* debian8

If you need a distro/version that is not listed, you can open a github issue so we can add it to the list.

Note: DEB package are currently only available for 64 bits architecture

Once repository is added, run command below to update package list.

```
apt-get update
```

Then install Synda package using command below

```
sudo apt-get install synda -y
```

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

Installing Synda from DEB package is multi-user (for single-user installation,
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
