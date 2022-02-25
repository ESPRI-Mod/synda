.. _conda-install:

Installation and upgrade
=========================

``synda`` is available on anaconda.



Requirements
************


Install an Anaconda distribution on your machine, step by step guide per OS available at:

.. code-block:: bash

    https://docs.conda.io/projects/conda/en/latest/user-guide/install/



Installation
*************

While undertaking the synda install via conda, please make sure you're using the proper
role for this. Using sudo might not be the best idea as it is not really required at all and
can interefere with other installation across the machine.

Create a synda isolated environment if you wish:

.. code-block:: bash

    conda create -n my-synda-environment python=3.9+

Activate the created environment:

.. code-block:: bash

    conda activate my-synda-environment


Then install ``synda`` package using command below:

.. code-block:: bash

    conda install -c ipsl -c conda-forge synda

.. note::

    Specify : -c **ipsl** -c **conda-forge** (i.e. *ipsl* and *conda-forge* anaconda channels) to get the right packages. Currently all dependencies are
    hosted on either default conda-forge anaconda channels or the ipsl channels to ease the installation.

Upgrade
************

Upgrade ``synda`` package using command below:

.. code-block:: bash

    conda update -c ipsl -c conda-forge synda
