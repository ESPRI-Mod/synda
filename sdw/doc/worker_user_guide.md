# *sdw* User Guide

## Dependencies

    pip install retrying python-jsonrpc python-daemon==1.6.1

## Configuration

Edit *worker* script and set variable below

* post-processing service default host (in argparse argument)
* post-processing service user and password
* daemon unprivileged user and group (optional)

## Configuration test

    ./worker -t

## Usage

    ./worker
