.. _rpm-install-sdt:

Installation from RPM package
=============================

Requirements
************

``synda`` RPM package is available for RHEL6 and RHEL7. On RHEL5, ``synda`` can only be installed from source.

Installation
************

EPEL repository must be installed.

To install EPEL, use

.. code-block:: bash

    sudo yum install epel-release -y

To install synda RPM package, use

.. code-block:: bash

    wget http://sd-53687.dedibox.fr/synda/sdt/rpm/<package-name>
    sudo yum install -y <package-name>

where <package-name> can be one of

-  synda-3.6-1.x86\_64\_centos65.rpm
-  synda-3.6-1.x86\_64\_centos67.rpm
-  synda-3.6-1.x86\_64\_centos71.rpm
-  synda-3.6-1.x86\_64\_fedora20.rpm
-  synda-3.6-1.x86\_64\_fedora21.rpm
-  synda-3.6-1.x86\_64\_fedora22.rpm
-  synda-3.6-1.x86\_64\_fedora23.rpm
-  synda-3.6-1.x86\_64\_scientific61.rpm
-  synda-3.6-1.x86\_64\_scientific67.rpm
-  synda-3.6-1.x86\_64\_scientific71.rpm

For example, to install ``synda`` on Scientific Linux 6.7, do

.. code-block:: bash

    sudo yum install http://sd-53687.dedibox.fr/synda/sdt/rpm/synda-3.6-1.x86_64_scientific67.rpm 

If you need a distribution/version that is not listed, you can open a GitHub (see :ref:`credits`) we can add it to the list.

.. note::

    RPM packages are currently only available for 64 bits architecture.

Configuration
*************

- Edit ``/etc/synda/sdt/credentials.conf``
- Edit ``/etc/synda/sdt/sdt.conf``

.. note::

    To download file from ESGF, you need to create an openID account on one ESGF identity provider website (e.g. PCMDI, BADC, DKRZ.) and subscribe to the project licence/role you want to download.

-  Restart service with

.. code-block:: bash

    sudo service sdt restart

- A quickstart guide is available with

.. code-block:: bash

    synda intro | more

.. note::

    To execute ``synda`` commands, you must either be root, or part of the synda group.

Files location
**************

.. code-block:: bash

    /etc/synda/sdt
    /srv/synda/sdt/data
    /srv/synda/sdt/sandbox
    /var/lib/synda/sdt
    /var/tmp/synda/sdt
    /var/tmp/synda/sdt/.esg/certificates
    /var/log/synda/sdt
    /usr/bin/synda
    /usr/share/python/synda/sdt
    /usr/share/doc/synda/sdt
