.. _selection-file-param-ref:

Selection file parameter reference
==================================

This document describes each parameter used in a selection file.

Search-api parameter
********************

Those parameters are described `here <https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API>`_

.. warning ::

    Those parameters are specific to Synda and cannot be used directly with the Search-api.

Synda download parameters
*************************

+----------------+----------+-------------------------------------------------------+-------------------------------------------------------------+
| Parameter      | Type     | Default value                                         | Function                                                    |
+================+==========+=======================================================+=============================================================+
| protocol       | *string* | http                                                  | HTTP is the only supported protocol.                        |
+----------------+----------+-------------------------------------------------------+-------------------------------------------------------------+
| searchapi_host | *string* | <index.default_index> from sdt.conf file              | Set which ESGF index to use for files discovery.            |
|                |          | or random index from <index.indexes> in parallel mode |                                                             |
+----------------+----------+-------------------------------------------------------+-------------------------------------------------------------+
| url_replace    | *string* |                                                       | Replace all occurrences of substring in url.                |
+----------------+----------+-------------------------------------------------------+-------------------------------------------------------------+
| priority       | *int*    | 1000                                                  | Set download priority.                                      |
+----------------+----------+-------------------------------------------------------+-------------------------------------------------------------+

Examples:

.. code-block:: text

    url_replace=s|gsiftp://esgf1.dkrz.de/data/cmip6|gsiftp://gridftp.dkrz.de/pool/data/projects/cmip6|

Synda remote search parameters
******************************

+-----------+----------+---------------+----------------------------------+
| Parameter | Type     | Default value | Function                         |
+===========+==========+===============+==================================+
| timeslice | *string* |               | Select files inside <timeslice>. |
+-----------+----------+---------------+----------------------------------+

Examples:

.. code-block:: bash

    synda search atmos mon tasmin CMIP5 CNRM-CM5 timeslice=197001-198512 -f

Synda local search parameters
*****************************

+--------------------+----------+---------------+---------------------------------------------+
| Parameter          | Type     | Default value | Function                                    |
+====================+==========+===============+=============================================+
| local_path         | *string* |               | Select files matching <local_path>.         |
+--------------------+----------+---------------+---------------------------------------------+
| error_msg          | *string* |               | Select files matching <error_msg>.          |
+--------------------+----------+---------------+---------------------------------------------+
| insertion_group_id | *int*    |               | Select files matching <insertion_group_id>. |
+--------------------+----------+---------------+---------------------------------------------+
| status             | *string* |               | Select files matching download <status>.    |
+--------------------+----------+---------------+---------------------------------------------+
| sdget_status       | *int*    |               | Select files matching <sdget_status>.       |
+--------------------+----------+---------------+---------------------------------------------+

Examples:

.. code-block:: bash

    synda list local_path=CMIP5/output1/NCAR/CCSM4/rcp60/mon/land/Lmon/r1i1p1
    synda list "error_msg=local file already exists," -f
    synda list insertion_group_id=71 -f
    synda list status=error -f
    synda list sdget_status=1 -f


Synda formatting parameters
***************************

+---------------------------+----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| Parameter                 | Type     | Default value | Function                                                                                                               |
+===========================+==========+===============+========================================================================================================================+
| local_path_format         | *string* | treevar       | Set local path format.                                                                                                 |
|                           |          |               | If set to "treevar", the dataset DRS is used to build the local path and a folder is added to group files by variable. |
|                           |          |               | If set to "tree", the dataset DRS is used to build the local path.                                                     |
|                           |          |               | If set to "custom", the local path is built based on template defined in <local_path_drs_template> variable.           |
|                           |          |               | If set to "notree", all files are stored in the same folder.                                                           |
+---------------------------+----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| local_path_product_format | *string* | normal        | If set to "normal", product folders (e.g. "output1" and "output2") are kept in local path.                             |
|                           |          |               | If set to "remove", product folders level are removed from local path and products sub-folders are merged.             |
|                           |          |               | If set to "merge", product folders are merged into one folder called "output" and products sub-folders are merged.     |
+---------------------------+----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| local_path_project_format | *string* | uc            | If set to "uc", local path project folder is converted to uppercase.                                                   |
+---------------------------+----------+---------------+------------------------------------------------------------------------------------------------------------------------+
| local_path_drs_template   | *string* |               | Contain the local path custom template.                                                                                |
+---------------------------+----------+---------------+------------------------------------------------------------------------------------------------------------------------+

Examples:

.. code-block:: text

    local_path_drs_template=%(ensemble)s/%(institute)s-%(rcm_name)s/%(rcm_version)s/%(time_frequency)s/%(variable)s/%(dataset_version)s

.. warning::

   To enable ``local_path_drs_template``, ``local_path_format`` parameter must be set to "custom". Each variable included in ``local_path_drs_template`` must be present as a standalone attribute in the file metadata. If it is missing, you can use a constant value instead (e.g. "output" instead of "%(product)s").
