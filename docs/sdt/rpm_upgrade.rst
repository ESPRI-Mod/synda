.. _rpm-upgrade-sdt:

Upgrade from RPM package
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

    sudo yum erase synda

Install new package version following :ref:`installation from RPM package <rpm-install-sdt>`.

Post-upgrade
************

Stop service with:

.. code-block:: bash

    sudo service sdt stop

As configuration files located in /etc/synda/sdt have been reinitialized during upgrade, you need to re-enter your openid and password, as well as any other parameter you may have set to a non-default value.

.. note::

    You can use a diff program to compare post-upgrade configuration files over pre-upgrade configuration files (from the backup).

Restore database from backup in ``/var/lib/synda/sdt`` (replace the existing file).

Restart service with:

.. code-block:: bash

    sudo service sdt restart
