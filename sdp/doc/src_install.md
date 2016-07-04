# *sdp* installation from source guide

## Introduction

This document describes how to install and configure sdp module.

## Synopsis

This documents contains instructions to install *sdp* from source.

## Requirements

Linux distribution with Python 2.6+.

## Dependencies

Install the following system packages (as root):

RHEL and derivative (Centos, Scientific Linux, Fedora..)

```
sudo yum install bc gcc python python-pip python-devel openssl-devel sqlite sqlite-devel zlib-devel libffi-devel
```

Debian and derivative (Ubuntu, Mint..)

```
sudo apt-get install bc gcc python python-pip python-dev libssl-dev sqlite3 libsqlite-dev libz-dev libffi-dev
```

## Installation

Install the application (as normal user or root):

    wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
    chmod +x ./install.sh
    ./install.sh postprocessing

## Configuration

* Run command below in $HOME/sdp/tmp folder

    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes

* Add lines below in your shell configuration file (e.g. '.bashrc')

```
export SP_HOME=$HOME/sdp
export PATH=$SP_HOME/bin:$PATH
```

## Files location

* $HOME/sdp/doc
* $HOME/sdp/bin
* $HOME/sdp/conf
* $HOME/sdp/db
* $HOME/sdp/log
* $HOME/sdp/tmp
