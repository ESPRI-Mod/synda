# Synda DEB package installation guide

## Synopsis

This documents contains instructions to install Synda from DEB package.

## Requirements

*synda* DEB package is available for Debian, Ubuntu and Mint.

## Installation

Add IPSL Synda repository

```
echo deb http://sd-53687.dedibox.fr/synda/sdt/deb/repo/<distro-name>/ ipslrepo contrib | sudo tee /etc/apt/sources.list.d/synda.list
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

## Patch

Synda 3.4 DEB package contains a bug which prevent displaying error messages under certain circumstances.

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
