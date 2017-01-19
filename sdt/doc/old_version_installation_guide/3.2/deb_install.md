# Synda 3.2 DEB package installation guide

## Synopsis

This documents contains instructions to install Synda from DEB package.

## Requirements

Synda DEB packages are available for Debian, Ubuntu and Mint.

## Installation

Add IPSL Synda repository

```
echo deb http://sd-104052.dedibox.fr/synda/deb/repo/<distro-name>/ ipslrepo contrib | sudo tee /etc/apt/sources.list.d/synda.list
```

where &lt;distro-name&gt; can be one of

* ubuntu14
* ubuntu12
* mint17
* debian8

If you need a distro/version that is not listed, you can open a github issue so we can add it to the list.

Note: DEB packages are currently only available for 64 bits architecture

Once repository is added, run command below to update package list.

```
sudo apt-get update
```

Then install Synda package using command below

```
sudo apt-get install synda --force-yes -y
```

### Patch

Synda 3.2 DEB package contains a bug which prevent running application under certain circumstances.

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
