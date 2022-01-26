.. _config-internal-param:

Internal parameters
*********************

This document describes each parameter listed in ``internal.conf`` file to configure Synda.


.. important::

    Parameters are grouped together in 6 sections : **logger**, **checksum**, **api**, **processes**, **hack** and **sub command get**.

notes
    Very few parameters might be customized. No guarantee of upward compatibility

logger
=========

``[logger].feeder_name``
    **Name** of the feeder **logger**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | feeder        |
    +-----------+---------------+

------------------

``[logger].consumer_name``
    **Name** of the consumer **logger**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | consumer      |
    +-----------+---------------+

------------------

``[logger].domain_name``
    **Name** of the domain **logger**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | domain        |
    +-----------+---------------+

------------------

``[logger].feeder_file``
    **Name** of the feeder **logger file**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | discovery.log |
    +-----------+---------------+

------------------

``[logger].consumer_file``
    **Name** of the consumer **logger file**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | transfer.log  |
    +-----------+---------------+

------------------

``[logger].domain_file``
    **Name** of the domain **logger file**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | domain.log    |
    +-----------+---------------+

checksum
=========

``[checksum].type_md5``
    **Name** for **md5** hash **type**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | md5           |
    +-----------+---------------+

------------------

``[checksum].type_sha256``
    **Name** for **sha256** hash **type**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | sha256        |
    +-----------+---------------+

api
=========

``[api].esgf_search_domain_name``
    **Domain** of the ESGF Search API.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | IDXHOSTMARK   |
    +-----------+---------------+

processes
===========

``[processes].chunksize``
    **Maximum number of files** returned after each call of the ESGF Search API.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 5000          |
    +-----------+---------------+

------------------

``[processes].http_client``
    Http **client**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | aiohttp       |
    +-----------+---------------+

------------------

``[processes].transfer_protocol``
    **Protocol** used for downloads.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | http          |
    +-----------+---------------+

------------------

``[processes].get_files_caching``
    **Enables** or **disables** caching mechanism.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | true      |
    +-----------+-----------+

hack
=========

``[hack].projects_with_one_variable_per_dataset``
    **List of projects** that meet the condition **one variable per dataset**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *string*  | CORDEX, CMIP6 |
    +-----------+---------------+

sub command get
==================

``[sub command get].display_downloads_progression_every_n_seconds``

    Frequency used for subcommand ``synda get [parameter]`` only.
    On the command line interface, the relevant data, when synda downloads files, is updated and displayed **every n seconds**.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 1             |
    +-----------+---------------+
