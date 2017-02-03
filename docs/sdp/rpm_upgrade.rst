.. _rpm-upgrade-sdp:

Upgrade from RPM package
========================

Pre-upgrade
***********

Stop service with:

.. code-block:: bash

   sudo service sdp stop

Backup folders below:

.. code-block:: bash

   /etc/synda/sdp
   /var/log/synda/sdp
   /var/lib/synda/sdp

Upgrade
*******

Remove previous package version:

.. code-block:: bash

    sudo yum erase synda_pp

Install new package version following :ref:`installation from RPM package <rpm-install-sdp>`.

Post-upgrade
************

Stop service with:

.. code-block:: bash

    sudo service sdp stop

As configuration files located in /etc/synda/sdp have been reinitialized during upgrade, you need to re-enter your username and password, as well as any other parameter you may have set to a non-default value.

.. note::

    You can use a diff program to compare post-upgrade configuration files over pre-upgrade configuration files (from the backup).

Restore database from backup in ``/var/lib/synda/sdp`` (replace the existing file).

Restart service with:

.. code-block:: bash

    sudo service sdp restart

