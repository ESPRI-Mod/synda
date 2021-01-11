.. _src-install-sdt:

Installation from source
========================

Requirements
************

Linux distribution with Python 2.6+.

A local file system should be preferred over a parallel distributed file system for the database file.

Dependencies
************

Install the following system packages (as root):

- for RHEL and derivative (CentOS, Scientific Linux, Fedora, etc.)

.. code-block:: bash

   sudo yum install bc gcc python python-pip python-devel openssl-devel sqlite sqlite-devel libxslt-devel libxml2-devel zlib-devel libffi-devel

- for Debian and derivative (Ubuntu, Mint, etc.)

.. code-block:: bash

   sudo apt-get install bc gcc python python-pip python-dev libssl-dev sqlite3 libsqlite-dev libxslt-dev libxml2-dev libz-dev libffi-dev

Installation
************

Install the application (as normal user or root):

.. code-block:: bash

    wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
    chmod +x ./install.sh
    ./install.sh

.. note::

   The ``-d`` option of the ``install.sh`` script can be used to install a specific version.

Patch
*****

``synda`` 3.6 source package contains a bug which prevent running application.

To fix it, downgrade the ``pillow`` package from 4.0 to 3.4.2 using command below:

.. code-block:: bash

    pip install pillow==3.4.2

Configuration
*************

- Add lines below in your shell configuration file (e.g. ``.bashrc``)

.. code-block:: bash

    export ST_HOME=$HOME/sdt
    export PATH=$ST_HOME/bin:$PATH

- Edit ``$ST_HOME/conf/credentials.conf`` file

.. note::

    To download file from ESGF, you need to untar an openID account on one ESGF identity provider website (e.g. PCMDI, BADC, DKRZ.) and subscribe to the project licence/role you want to download.

- A quickstart guide is available with

.. code-block:: bash

    synda intro | more

Files location
**************

.. code-block:: bash

    $HOME/sdt/doc
    $HOME/sdt/bin
    $HOME/sdt/conf
    $HOME/sdt/data
    $HOME/sdt/db
    $HOME/sdt/log
    $HOME/sdt/tmp
    $HOME/sdt/tmp/.esg
    $HOME/sdt/tmp/.esg/certificates
