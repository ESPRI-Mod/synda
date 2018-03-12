# Synda upgrade guide (installation from source)

## Synopsis

This document contains instructions to install new Synda version.

## Procedure

### Pre-upgrade

Backup $ST_HOME folder ($HOME/sdt)

### Upgrade

Run commands below:

    mkdir inst_tmpdir
    cd inst_tmpdir
    wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
    chmod +x install.sh
    ./install.sh -u transfer

### Post-upgrade

As configuration files located in $ST_HOME/conf may have been reinitialized
during upgrade, you need to check if parameters are still correctly set (e.g.
openid, password..).

Note: you can use a diff program to compare post-upgrade configuration files
over pre-upgrade configuration files (from the backup).
