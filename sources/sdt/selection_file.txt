.. _selection-file:

Selection file
==============

A selection file contains parameters to define which data you want to
download from ESGF archive, how to download it and how to store the
data.

The user defines one or many selection files. Each of them have a list
of facets (variables, frequencies, experiments, ensemble, model, etc.).
Using them, the program explore the ESGF archive and download all the
corresponding available files. The program may be run regularly to
download the possible new files. Typically each file is associated with
an analysis (cfmip, downscaling and so on). Create as many selection
files as you want in the "selection" folder.

Those selection files are stored in ``$HOME/sdt/selection`` folder (source
installation) or ``/etc/synda/sdt/selection`` (system package
installation).

Example of a selection file

.. code-block:: text

    project=CMIP5
    model=CNRM-CM5 CSIRO-Mk3-6-0
    experiment=historical amip
    ensemble=r1i1p1
    variable[atmos][mon]=tasmin tas psl
    variable[ocean][fx]=areacello sftof
    variable[land][mon]=mrsos nppRoot nep

.. note::

    Many selection file examples can be found `here <https://github.com/Prodiguer/synda/tree/master/sdt/selection/sample>`_. Selection files are sometimes called "template" or "selection form".

Selection file format
*********************

A selection file accepts the four following line formats.

Realm frequency and variable(s)
-------------------------------

Definition:

.. code-block:: text

    variable[<realm>][<frequency>]=<variable1> <variable2> [...]

Example:

.. code-block:: text

    variable[atmos][mon]=tas psl tasmin

.. note::

    Space is used as variable delimiter.

Facet(s) and variable(s)
------------------------

Definition:

.. code-block:: text

    variable[<facet1> <facet2> <facet3> [...]]=<variable1> <variable2> [...]

Example:

.. code-block:: text

    variable[rcp26 atmos mon]=tasmin tasmax

.. note::

    Space is used as facets and variables delimiter.

Name and value
--------------

Definition:

.. code-block:: text

    <name>=<value>

Example:

.. code-block:: text

    experiment=rcp26

Standalone value
----------------

Definition:

.. code-block:: text

    <value>

Example:

.. code-block:: text

    rcp26

.. warning::

    Blank line are ignored. Selection files may include comments, prefixed by specific characters. Trailing comments are not supported.

Selection file parameter
************************

See :ref:`selection file parameter reference <selection-file-param-ref>`.

Selection file management
*************************

Adding a selection file
-----------------------

Create a new selection file in the "selection" folder and set the filters.

Then run command below to start the discovery:

.. code-block:: bash

    synda install -s <selection-file>

Editing a selection file
------------------------

Edit the file and change filters accordingly.

Then run command below:

.. code-block:: bash

    synda install -s <selection-file>

Removing a selection file
-------------------------

Run command below to remove files matching the selection file

.. code-block:: bash

    synda remove -s <selection-file>

Then manually remove the selection file from the "selection" folder.
