# Synda upgrade guide

## Synopsis

This documents contains instructions to install the new Synda software version.

## Procedure

### Pre-upgrade

Backup $ST_HOME folder (e.g. $HOME/sdt)

### Upgrade

Run commands below:

    mkdir inst_tmpdir
    cd $inst_tmpdir
    wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
    chmod +x install.sh
    ./install.sh -u transfer

### Post-upgrade

As configuration files located in $ST_HOME/conf may have been reinitialized
during installation, you need to check if parameters are still correctly set
(e.g. openid).

Note: you can use a diff program to compare post-upgrade configuration files
over backuped pre-upgrade configuration files.
