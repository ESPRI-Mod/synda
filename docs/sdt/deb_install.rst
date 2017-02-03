.. _deb-install-sdt:

Installation from DEB package
=============================

Requirements
************

``synda`` DEB package is available for Debian, Ubuntu and Mint.

Installation
************

Add IPSL Synda repository

.. code-block:: bash

    echo deb http://sd-53687.dedibox.fr/synda/sdt/deb/repo/<distro-name>/ ipslrepo contrib | sudo tee /etc/apt/sources.list.d/synda.list

where <distro-name> can be one of

- ubuntu14
- ubuntu12
- mint17
- debian8

If you need a distribution/version that is not listed, you can open a GitHub (see :ref:`credits`) we can add it to the list.

.. note::

    DEB packages are currently only available for 64 bits architecture

Once repository is added, run command below to update the package list:

.. code-block:: bash

    sudo apt-get update

Then install ``synda`` package using command below:

.. code-block:: bash

    sudo apt-get install synda --force-yes -y

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
