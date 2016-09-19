# *sdp* DEB package installation guide

## Synopsis

This documents contains instructions to install *sdp* from DEB package.

## Requirements

*sdp* DEB package is available for Debian, Ubuntu and Mint.

## Terminology

* *synda* is the application name
* *sdp* is the module name (synda is made of several modules)
* *synda-pp* is the Debian package name

## Installation

Add IPSL Synda repository

```
echo deb http://sd-53687.dedibox.fr/synda/sdp/deb/repo/<distro-name>/ ipslrepo contrib | sudo tee /etc/apt/sources.list.d/synda-pp.list
```

where &lt;distro-name&gt; can be one of

* ubuntu14
* ubuntu12
* mint17
* debian8

If you need a distro/version that is not listed, you can open a github issue so we can add it to the list.

Note: DEB packages are currently only available for 64 bits architecture

Once repository is added, run command below to update the package list.

```
sudo apt-get update
```

Then install synda-pp package using command below

```
sudo apt-get install synda-pp --force-yes -y
```

## Configuration

* Edit */etc/synda/sdp/sdp.conf* file

* Restart service with

```
sudo service sdp restart
```

## Files location

* /etc/synda/sdp
* /var/lib/synda/sdp
* /var/tmp/synda/sdp
* /var/log/synda/sdp
* /usr/bin/synda_pp
* /usr/share/python/synda/sdp
* /usr/share/doc/synda/sdp
