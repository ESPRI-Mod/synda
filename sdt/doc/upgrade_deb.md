# Synda Debian package upgrade guide

## Synopsis

This document contains instructions to upgrade Synda version using Debian package.

## Procedure

### Pre-upgrade

Backup folders below

    /etc/synda/sdt
    /var/log/synda/sdt

### Upgrade

Remove previous package version using command below:

    dpkg -P synda

Install new package version using [this guide](deb_install.md)

### Post-upgrade

As configuration files located in /etc/synda/sdt have been reinitialized
during upgrade, you need to re-enter your openid and password, as well as any
other parameter you may have changed.

Note: you can use a diff program to compare post-upgrade configuration files
over pre-upgrade configuration files (from the backup).
