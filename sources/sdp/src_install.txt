.. _src-install-sdp:

Installation from source
========================

Requirements
************

Linux distribution with Python 2.6+.

A local file system should be preferred over a parallel distributed file system for the database file.

Dependencies
************

Install the following system packages (as root):

- for RHEL and derivative (Centos, Scientific Linux, Fedora, etc.)

.. code-block:: bash

   sudo yum install bc gcc python python-pip python-devel openssl-devel sqlite sqlite-devel zlib-devel libffi-devel

- for Debian and derivative (Ubuntu, Mint, etc.)

.. code-block:: bash

   sudo apt-get install bc gcc python python-pip python-dev libssl-dev sqlite3 libsqlite-dev libz-dev libffi-dev

Installation
************

Install the application (as normal user or root):

.. code-block:: bash

   wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
   chmod +x ./install.sh
   ./install.sh postprocessing

.. note::

   The ``-d`` option of the ``install.sh`` script can be used to install a specific version.

Configuration
*************

- Run command below in ``$HOME/sdp/tmp`` folder:

.. code-block:: bash

   openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes


- Add lines below in your shell configuration file (e.g. '.bashrc')

.. code-block:: bash

   export SP_HOME=$HOME/sdp
   export PATH=$SP_HOME/bin:$PATH

Files location
**************

.. code-block:: bash

    $HOME/sdp/doc
    $HOME/sdp/bin
    $HOME/sdp/conf
    $HOME/sdp/db
    $HOME/sdp/log
    $HOME/sdp/tmp