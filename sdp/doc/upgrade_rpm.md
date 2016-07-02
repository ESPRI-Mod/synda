# *sdp* RPM package upgrade guide

## Synopsis

This document contains instructions to upgrade *sdp* version using RPM package.

## Procedure

### Pre-upgrade

Backup folders below

    /etc/synda/sdp
    /var/log/synda/sdp
    /var/lib/synda/sdp

### Upgrade

Remove previous package version using command below:

    sudo yum erase synda

Install new package version using [this guide](rpm_install.md)

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
