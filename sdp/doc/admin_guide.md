# Synda Post-Processing - administration guide

## Introduction

This document describes how to install and configure Synda Post-Processing
module.

## Installation

Install dependencies with

    yum install gcc python python-pip python-devel openssl-devel sqlite sqlite-devel zlib-devel libffi-devel

Install Synda Post-Processing module with

    wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
    chmod +x ./install.sh
    ./install.sh postprocessing

## Configuration

Run command below in $HOME/sdp/tmp folder

    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
