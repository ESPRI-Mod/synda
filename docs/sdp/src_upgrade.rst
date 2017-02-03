.. _src-upgrade-sdp:

Upgrade from source
===================

Pre-upgrade
***********

Stop daemon with:

.. code-block:: bash

    spdaemon stop

Backup ``$HOME/sdp`` folder.

Upgrade
*******

Run commands below:

.. code-block:: bash

   mkdir inst_tmpdir
   cd inst_tmpdir
   wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
   chmod +x install.sh
   ./install.sh -u postprocessing

Post-upgrade
************

As configuration files located in $HOME/sdp/conf may have been reinitialized during upgrade, you need to check if parameters are still correctly set (e.g. username, password, etc.).

.. note::

    You can use a diff program to compare post-upgrade configuration files over pre-upgrade configuration files (from the backup).

Start daemon with:

.. code-block:: bash

    spdaemon start
