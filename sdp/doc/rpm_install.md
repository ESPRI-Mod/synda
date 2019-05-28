# *sdp* RPM package installation guide

## Synopsis

This documents contains instructions to install *sdp* from RPM package.

## Requirements

*sdp* RPM package is available for RHEL6 and RHEL7.

On RHEL5, *sdp* can only be installed from source.

## Terminology

* *synda* is the application name
* *sdp* is the module name (synda is made of several modules)
* *synda-pp* is the RPM package name

## Installation

EPEL repository must be installed.

To install EPEL, use

```
sudo yum install epel-release -y
```

To install *sdp* RPM package, use

```
wget http://sd-104052.dedibox.fr/synda/sdp/rpm/<package-name>
sudo yum install -y <package-name>
```

where &lt;package-name&gt; can be one of

* synda-pp-1.2-1.x86_64_centos65.rpm
* synda-pp-1.2-1.x86_64_centos67.rpm
* synda-pp-1.2-1.x86_64_centos71.rpm
* synda-pp-1.2-1.x86_64_fedora20.rpm
* synda-pp-1.2-1.x86_64_fedora21.rpm
* synda-pp-1.2-1.x86_64_fedora22.rpm
* synda-pp-1.2-1.x86_64_fedora23.rpm
* synda-pp-1.2-1.x86_64_scientific61.rpm
* synda-pp-1.2-1.x86_64_scientific67.rpm
* synda-pp-1.2-1.x86_64_scientific71.rpm

Example

To install *sdp* on Scientific Linux 6.7, do

```
sudo yum install http://sd-104052.dedibox.fr/synda/sdp/rpm/synda-pp-1.2-1.x86_64_scientific67.rpm 
```

If you need a distro/version that is not listed, you can open a github issue so we can add it to the list.

Note: RPM packages are currently only available for 64 bits architecture

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
