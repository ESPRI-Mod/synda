# Synda installation from source guide

## Synopsis

This documents contains instructions to install Synda from source.

## Requirements

Linux distribution with Python 2.6+.

A local file system should be preferred over a parallel distributed file system
for the database file.

## Dependencies

Install the following system packages (as root):

RHEL and derivative (Centos, Scientific Linux, Fedora..)

```
sudo yum install bc gcc python python-pip python-devel openssl-devel sqlite sqlite-devel libxslt-devel libxml2-devel zlib-devel libffi-devel
```

Debian and derivative (Ubuntu, Mint..)

```
sudo apt-get install bc gcc python python-pip python-dev libssl-dev sqlite3 libsqlite-dev libxslt-dev libxml2-dev libz-dev libffi-dev
```

## Installation

Install the application (as normal user or root):

```
wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
chmod +x ./install.sh
./install.sh
```

Note: the ```-d``` option of the ```install.sh``` script can be used to install a specific version.

### Patch

Synda 3.6 source package contains a bug which prevent running application.

To fix it, downgrade the ```pillow``` package from 4.0 to 3.4.2 using command below

    pip install pillow==3.4.2

## Configuration

* Add lines below in your shell configuration file (e.g. '.bashrc')

```
export ST_HOME=$HOME/sdt
export PATH=$ST_HOME/bin:$PATH
```

* Edit credentials file to set openid and password (ESGF credential)

```
vi $ST_HOME/conf/credentials.conf
```

Note: to download file from ESGF, you need to create an openID account on one
ESGF identity provider website (e.g. PCMDI, BADC or DKRZ) and subscribe to
CMIP5-RESEARCH role.

## Usage

A quickstart guide is available by running 'intro' subcommand

```
synda intro | more
```

## Files location

* $HOME/sdt/doc
* $HOME/sdt/bin
* $HOME/sdt/conf
* $HOME/sdt/data
* $HOME/sdt/db
* $HOME/sdt/log
* $HOME/sdt/tmp
* $HOME/sdt/tmp/.esg
* $HOME/sdt/tmp/.esg/certificates
