.. _deb-install-sdt:

Installation from conda package
===============================

``synda transfer module`` is now available on anaconda.



Requirements
************


Install an Anaconda distribution on your machine, step by step guide per OS available at:

.. code-block:: bash

    https://docs.conda.io/projects/conda/en/latest/user-guide/install/



Installation
************

While undertaking the synda install via conda, please make sure you're using the proper
role for this. Using sudo might not be the best idea as it is not really required at all and
can interefere with other installation across the machine.

Create a synda isolated environment if you wish:

.. code-block:: bash

    conda create --name my-synda-envrionment python=2.7

Activate the created environment:

.. code-block:: bash

    conda activate my-synda-environment


Then install ``synda`` package using command below:

.. code-block:: bash

    conda install -c IPSL synda

.. note::

    Specifying -c IPSL is using the IPSL anaconda channel to get the right package. Currently all dependencies are
    hosted on either default anaconda channels or the IPSL channels to ease the installation.

Configuration
*************

Now the package is installed, you'll need to properly configure the synda work environment.
To do so, the first step is the set a synda home environment variable. This will the be the directory
that will harbor all the configuration, database and other required files for synda to function properly.
So choose it well. For instance: ``/home/user/.synda`` would do the trick.

.. code-block:: bash

    export ST_HOME=/path/to/synda_home_directory

At this point Synda can perform basic functions. But will still require at least initializing the stubs of the required
files.
The structure of synda home directory should be as follows:

.. code-block:: bash

    > tree $ST_HOME

    ├── bin
    │   ├── sdcleanup_tree.sh
    │   ├── sdconvert.sh
    │   ├── sdgetg.sh
    │   ├── sdget.sh
    │   └── sdparsewgetoutput.sh
    ├── conf
    │   ├── credentials.conf
    │   ├── default
    │   │   ├── default_CMIP5.txt
    │   │   └── default.txt
    │   └── sdt.conf
    ├── data
    ├── db
    │   └── sdt.db
    ├── log
    │   ├── debug.log
    │   ├── discovery.log
    │   ├── domain.log
    │   └── transfer.log
    ├── sandbox
    ├── selection
    │   └── sample
    │       ├── sample_selection_01.txt
    │       ├── sample_selection_02.txt
    │       ├── sample_selection_03.txt
    │       ├── sample_selection_04.txt
    │       ├── sample_selection_05.txt
    │       ├── sample_selection_06.txt
    │       ├── sample_selection_07.txt
    │       ├── sample_selection_08.txt
    │       ├── sample_selection_09.txt
    │       └── sample_selection_10.txt
    └── tmp

Whether this is an upgrade install or a from scratch install this is how the directory tree should look.
In case of a from scratch install, synda can init the environment for you at the first run of any synda command.


.. code-block:: bash

    > synda -h
    Synda has issues reaching your credential file, in ST_HOME.
    Running synda checking environment tool...
    Key file missing: bin/sdcleanup_tree.sh
    You can either copy previously used file into your ST_HOME (/root/.synda) or use synda init-env command to
    initialize a new synda home file system with stubs to fill properly.
    Synda environment needs a few key files.
    Would you like to init the stubs of these files? y/n:

In case the user replies positively, a directory will be created under ST_HOME with file stubs that need to be
filled properly afterwards. Especially the openID credentials. Which can also be used interactively using synda.

.. code-block:: bash

    >synda check-env
    Would you like to set your openID credentials? y/n: y
    openID url: https://open-id.url.com
    password: some_strong_password
    Check complete.

This can also be done manually the old fashion way if the users wish to do so.
