.. _selection-file-param-ref:

Selection file parameter reference
==================================

This document describes each parameter used in a selection file.

The ESGF Search-api parameters are described `here <https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API>`_

.. warning ::

    Those parameters are specific to Synda and cannot be used directly with the Search-api.

Synda download parameters
*************************

``protocol``
    Select which protocol to use to download the data.

    The two currently supported protocols are HTTP and GridFTP.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | http          |
    +-----------+---------------+

------------------

``searchapi_host``
    Set which ESGF index to use for files discovery.

    +-----------+------------------------------------------+
    | Type      | Default                                  |
    +===========+==========================================+
    | *string*  | <index.default_index> from sdt.conf file |
    +-----------+------------------------------------------+

------------------

``url_replace``
    Replace all occurrences of substring in url.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  |               |
    +-----------+---------------+

------------------

``priority``
    Set download priority.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 1000          |
    +-----------+---------------+

Example :

.. code-block:: text

    url_replace=s|gsiftp://esgf1.dkrz.de/data/cmip6|gsiftp://gridftp.dkrz.de/pool/data/projects/cmip6|

Synda remote search parameters
******************************

``timeslice``
    Select files inside <timeslice>.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  |               |
    +-----------+---------------+

Example :

.. code-block:: bash

    synda search atmos mon tasmin CMIP5 CNRM-CM5 timeslice=197001-198512 -f

Synda local search parameters
*****************************

``local_path``
    Select files matching <local_path>.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  |               |
    +-----------+---------------+

------------------

``error_msg``
    Select files matching <error_msg>.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  |               |
    +-----------+---------------+

------------------

``status``
    Select files matching download <status>.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  |               |
    +-----------+---------------+

------------------

``insertion_group_id``
    Select files matching <insertion_group_id>.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     |               |
    +-----------+---------------+

------------------

``sdget_status``
    Select files matching <sdget_status>.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     |               |
    +-----------+---------------+

Examples :

.. code-block:: bash

    synda list local_path=CMIP5/output1/NCAR/CCSM4/rcp60/mon/land/Lmon/r1i1p1
    synda list "error_msg=local file already exists," -f
    synda list insertion_group_id=71 -f
    synda list status=error -f
    synda list sdget_status=1 -f


Synda formatting parameters
***************************

``local_path_format``
    **treevar**

    If set to "treevar", the dataset DRS is used to build the local path and a folder is added to group files by variable.

    **tree**

    If set to "tree", the dataset DRS is used to build the local path.

    **custom**

    If set to "custom", the local path is built based on template defined in <local_path_drs_template> variable.

    **notree**

    If set to "notree", all files are stored in the same folder.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | treevar       |
    +-----------+---------------+

------------------

``local_path_product_format``
    **normal**

    If set to "normal", product folders (e.g. "output1" and "output2") are kept in local path.

    **remove**

    If set to "remove", product folders level are removed from local path and products sub-folders are merged.

    **merge**

    If set to "merge", product folders are merged into one folder called "output" and products sub-folders are merged.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | normal        |
    +-----------+---------------+

------------------

``local_path_project_format``
    **uc**

    If set to "uc", local path project folder is converted to uppercase.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | uc            |
    +-----------+---------------+

------------------

``local_path_drs_template``
    Contain the local path custom template.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  |               |
    +-----------+---------------+

Example :

.. code-block:: text

    local_path_drs_template=%(ensemble)s/%(institute)s-%(rcm_name)s/%(rcm_version)s/%(time_frequency)s/%(variable)s/%(dataset_version)s

.. warning::

   To enable ``local_path_drs_template``, ``local_path_format`` parameter must be set to "custom". Each variable included in ``local_path_drs_template`` must be present as a standalone attribute in the file metadata. If it is missing, you can use a constant value instead (e.g. "output" instead of "%(product)s").
