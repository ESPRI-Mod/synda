# Synda RPM package upgrade guide

## Synopsis

This document contains instructions to upgrade Synda version using RPM package.

## Procedure

### Pre-upgrade

Backup folders below

    /etc/synda/sdt
    /var/log/synda/sdt
    /var/lib/synda/sdt

### Upgrade

Remove previous package version using command below:

    sudo yum erase synda

Install new package version using [this guide](rpm_install.md)

### Post-upgrade

Stop service with

```
sudo service synda stop
```

As configuration files located in /etc/synda/sdt have been reinitialized
during upgrade, you need to re-enter your openid and password, as well as any
other parameter you may have set to a non-default value.

Note: you can use a diff program to compare post-upgrade configuration files
over pre-upgrade configuration files (from the backup).

Restore database from backup in /var/lib/synda/sdt (replace the existing file).

Restart service with

```
sudo service synda restart
```
