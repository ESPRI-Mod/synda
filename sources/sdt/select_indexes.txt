.. _select-indexes:

ESGF index selection
====================

Synda index settings are stored in ``sdt.conf`` in [index] section.

- ``default_index`` parameter is used for interactive search operations.
- ``indexes`` parameter is used for parallel searches (to improve response time by distributing queries on several indexes simultaneously).

.. note:

    Host set in ``default_index`` parameter can also be set in ``indexes`` parameter (i.e. same host can be used at both places).

.. code-block:: text

    [index]
    default_index=<idx>
    indexes=<idx1>, <idx2>, [...]

ESGF main indexes
*****************

-  esg-datanode.jpl.nasa.gov
-  esgf-node.ipsl.fr
-  esgf-data.dkrz.de
-  esgf-index1.ceda.ac.uk
-  esg.ccs.ornl.gov

ESGF indexes complete list
**************************

To display complete ESGF index list, use command below:

.. code-block:: bash

    synda param index_node
