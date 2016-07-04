# *sdp* DEB package upgrade guide

## Synopsis

This document contains instructions to upgrade *sdp* version using Debian package.

## Procedure

### Pre-upgrade

Backup folders below

    /etc/synda/sdp
    /var/log/synda/sdp
    /var/lib/synda/sdp

### Upgrade

Remove previous package version

    sudo dpkg -P synda-pp

Install new package version using [this guide](deb_install.md)

### Post-upgrade

Stop service with

```
sudo service sdp stop
```

As configuration files located in /etc/synda/sdp have been reinitialized
during upgrade, you need to re-enter your username and password, as well as any
other parameter you may have set to a non-default value.

Note: you can use a diff program to compare post-upgrade configuration files
over pre-upgrade configuration files (from the backup).

Restore database from backup in /var/lib/synda/sdp (replace the existing file).

Restart service with

```
sudo service sdp restart
```
