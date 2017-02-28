.. _deb-upgrade-sdt:

Upgrade from DEB package
========================

Pre-upgrade
***********

Stop service with:

.. code-block:: bash

   sudo service sdt stop

Backup folders below:

.. code-block:: bash

   /etc/synda/sdt
   /var/log/synda/sdt
   /var/lib/synda/sdt

Upgrade
*******

Remove previous package version:

.. code-block:: bash

    sudo dpkg -P synda

Install new package version following :ref:`installation from DEB package <deb-install-sdt>`.

Post-upgrade
************

Stop service with:

.. code-block:: bash

    sudo service sdt stop

As configuration files located in /etc/synda/sdt have been reinitialized during upgrade, you need to re-enter your username and password, as well as any other parameter you may have set to a non-default value.

.. note::
    You can use a diff program to compare post-upgrade configuration files over pre-upgrade configuration files (from the backup).

Restore database from backup in ``/var/lib/synda/sdt`` (replace the existing file).

Run commands below as root to set group permission on Synda data :

.. code-block:: bash

    find /srv/synda/sdt -print0 | xargs -0 chown :synda
    find /srv/synda/sdt -type d -print0 | xargs -0 chmod g+ws

Restart service with:

.. code-block:: bash

    sudo service sdt restart
