.. _rpm-install-sdp:

Installation from RPM package
=============================

Requirements
************

``synda_pp`` RPM package is available for RHEL6 and RHEL7. On RHEL5, ``synda_pp`` can only be installed from source.

Installation
************

EPEL repository must be installed.

To install EPEL, use:

.. code-block:: bash

   sudo yum install epel-release -y

To install ``sdp`` RPM package, use:

.. code-block:: bash

   wget http://sd-104052.dedibox.fr/synda/sdp/rpm/<package-name>
   sudo yum install -y <package-name>

where <package-name> can be one of

-  synda-pp-1.3-1.x86\_64\_centos65.rpm
-  synda-pp-1.3-1.x86\_64\_centos67.rpm
-  synda-pp-1.3-1.x86\_64\_centos71.rpm
-  synda-pp-1.3-1.x86\_64\_fedora20.rpm
-  synda-pp-1.3-1.x86\_64\_fedora21.rpm
-  synda-pp-1.3-1.x86\_64\_fedora22.rpm
-  synda-pp-1.3-1.x86\_64\_fedora23.rpm
-  synda-pp-1.3-1.x86\_64\_scientific61.rpm
-  synda-pp-1.3-1.x86\_64\_scientific67.rpm
-  synda-pp-1.3-1.x86\_64\_scientific71.rpm

For example, to install ``synda_pp`` on Scientific Linux 6.7, do:

.. code-block:: bash

   sudo yum install http://sd-104052.dedibox.fr/synda/sdp/rpm/synda-pp-1.3-1.x86_64_scientific67.rpm

If you need a distribution/version that is not listed, you can open a GitHub (see :ref:`credits`) we can add it to the list.

.. note::

    RPM packages are currently only available for 64 bits architecture.

Configuration
*************

- Edit ``/etc/synda/sdp/sdp.conf`` file
- Restart service with:

.. code-block:: bash

   sudo service sdp restart

Files location
**************

.. code-block:: bash

   /etc/synda/sdp
   /var/lib/synda/sdp
   /var/tmp/synda/sdp
   /var/log/synda/sdp
   /usr/bin/synda\_pp
   /usr/share/python/synda/sdp
   /usr/share/doc/synda/sdp
