# Synda upgrade guide

## Synopsis

    This documents contains instructions to install the new Synda software version.

## Procedure

### 1. Backup $ST_HOME folder (e.g. $HOME/sdt)

### 2. Run commands below

    mkdir inst_tmpdir
    cd $inst_tmpdir
    wget https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
    chmod +x install.sh
    ./install.sh -u transfer

### 3. Check configuration files

As configuration files located in $ST_HOME/conf may have been reinitialized
during installation, you need to check if parameters are still correctly set
(e.g. openid).

Note: you can use a diff program to compare post-upgrade configuration files
over pre-upgrade configuration files (from the backup).
