.. _deb-install-sdp:

Installation from DEB package
=============================

Requirements
************

``synda_pp`` DEB package is available for Debian, Ubuntu and Mint.

Installation
************

Add IPSL Synda repository

.. code-block:: bash

    echo deb http://sd-104052.dedibox.fr/synda/sdp/deb/repo/<distro-name>/ ipslrepo contrib | sudo tee /etc/apt/sources.list.d/synda-pp.list

where <distro-name> can be one of

- ubuntu14
- ubuntu12
- mint17
- debian8

If you need a distribution/version that is not listed, you can open a GitHub (see :ref:`credits`) we can add it to the list.

.. note::

    DEB packages are currently only available for 64 bits architecture.

Once repository is added, run command below to update the package list:

.. code-block:: bash

    sudo apt-get update

Then install ``synda-pp`` package using command below:

.. code-block:: bash

    sudo apt-get install synda-pp --force-yes -y

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
