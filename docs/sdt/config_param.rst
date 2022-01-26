.. _config-param:

User Preferences
*****************

This document describes each parameter listed in ``sdt.conf`` file to configure Synda.

.. important::

    Parameters are grouped together in 9 sections : **download**, **log**, **core**, **interface**, **behaviour**, **index**, **api**, **locale** and **install**.

notes
  The ``$ST_HOME`` linux variable contains the path of your local Synda environment.

download
=========

``[download].max_parallel_download``
    Set the **number** of parallel download.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 8             |
    +-----------+---------------+

------------------

``[download].url_max_buffer_size``
    Limit buffer **size** as apache server doesnt support more than 4000 chars for HTTP GET buffer.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 3500          |
    +-----------+---------------+

------------------

``[download].direct_http_timeout``
    Direct download HTTP timeout, in seconds, when Synda is waiting for the HTTP response.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 30            |
    +-----------+---------------+

------------------

``[download].async_http_timeout``
    Asynchronous download HTTP timeout, in seconds, when Synda is waiting for the HTTP response.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 120           |
    +-----------+---------------+

------------------

``[download].direct_db_timeout``
    This timeout parameter specifies how long, in seconds, the connection should wait for the lock to go away until raising an exception.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 120           |
    +-----------+---------------+

------------------

``[download].async_db_timeout``
    This timeout parameter specifies how long, in seconds, the connection should wait for the lock to go away until raising an exception.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 120           |
    +-----------+---------------+

------------------

``[download].streaming_chunk_size``
    Files are downloaded into several parts to not exceed a max memory level. **streaming_chunk_size** characterizes the size of each part (i.e. the data size of each http response).

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 0             |
    +-----------+---------------+

------------------

``[download].http_fallback``
    If GridFTP transfer fails, GridFTP URL is automatically replaced with HTTP URL.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | false     |
    +-----------+-----------+

------------------

``[download].download``
    If true, download files from ESGF.
    To use synda in discovery only, set this parameter to false.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | true      |
    +-----------+-----------+

log
=========

``[log].verbosity_level``
    Log verbosity **level**.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | info                     |
    +-----------+--------------------------+

------------------

``[log].scheduler_profiling``
    Log code profiling information.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | false     |
    +-----------+-----------+

core
=========

``[core].metadata_server_type``
    Type of metadata server.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | esgf_search_api          |
    +-----------+--------------------------+

------------------

``[core].default_path``
    Default selection files directory **path**.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | ``$ST_HOME/conf/default``|
    +-----------+--------------------------+

------------------

``[core].selection_path``
    Selection files directory **path**.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | ``$ST_HOME/selection``   |
    +-----------+--------------------------+

------------------

``[core].data_path``
    Data directory **path**.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | ``$ST_HOME/data``        |
    +-----------+--------------------------+

------------------

``[core].db_path``
    Database directory **path**.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | ``$ST_HOME/db``          |
    +-----------+--------------------------+

------------------

``[core].sandbox_path``
    Sandbox directory **path**.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | ``$ST_HOME/sandbox``     |
    +-----------+--------------------------+

interface
=========

``[interface].unicode_term``
    Use unicode characters for progress bar.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | false     |
    +-----------+-----------+

------------------

``[interface].progress``
    Show progress bar for time consuming task.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | false     |
    +-----------+-----------+

------------------

``[interface].show_advanced_options``
    Allow selection of advanced options associated with some subcommands.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | false     |
    +-----------+-----------+

------------------

``[interface].default_listing_size``
    This parameter drives how many results are displayed by default for "search", "list" and "dump" subcommands.

    +-----------+-------------+--------------------------+
    | Type      | Default     | Possible values          |
    +===========+=============+==========================+
    | *string*  | small       |  small | medium | big    |
    +-----------+-------------+--------------------------+

------------------

``[interface].dump_listing_limit_for_small_mode``
    This parameter drives how many results are displayed by default in small mode for "dump" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 50            |
    +-----------+---------------+

------------------

``[interface].dump_listing_limit_for_medium_mode``
    This parameter drives how many results are displayed by default in medium mode for "dump" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 100           |
    +-----------+---------------+

------------------

``[interface].dump_listing_limit_for_big_mode``
    This parameter drives how many results are displayed by default in big mode for "dump" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 6000          |
    +-----------+---------------+

------------------

``[interface].list_listing_limit_for_small_mode``
    This parameter drives how many results are displayed by default in small mode for "list" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 20            |
    +-----------+---------------+

------------------

``[interface].list_listing_limit_for_medium_mode``
    This parameter drives how many results are displayed by default in medium mode for "list" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 200           |
    +-----------+---------------+

------------------

``[interface].list_listing_limit_for_big_mode``
    This parameter drives how many results are displayed by default in big mode for "list" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 20000         |
    +-----------+---------------+

------------------

``[interface].search_listing_limit_for_small_mode``
    This parameter drives how many results are displayed by default in small mode for "search" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 100           |
    +-----------+---------------+

------------------

``[interface].search_listing_limit_for_medium_mode``
    This parameter drives how many results are displayed by default in medium mode for "search" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 1000          |
    +-----------+---------------+

------------------

``[interface].search_listing_limit_for_big_mode``
    This parameter drives how many results are displayed by default in big mode for "search" subcommand.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 6000          |
    +-----------+---------------+

behaviour
===========

``[behaviour].onemgf``
    Improve search performance.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | false     |
    +-----------+-----------+

------------------

``[behaviour].check_parameter``
    Perform parameter typo detection (name and value).

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | false     |
    +-----------+-----------+

------------------

``[behaviour].ignorecase``
    Automatically fix incorrect case.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | true      |
    +-----------+-----------+

------------------

``[behaviour].nearest``
    Automatically select the nearest file replica.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | false     |
    +-----------+-----------+

------------------

``[behaviour].nearest_mode``
    Set nearest replica algorithm.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | geolocation              |
    +-----------+--------------------------+

------------------

``[behaviour].lfae_mode``
    Set which policies to adopt when a download starts and local file already exists (lfae).

    +-----------+-------------+--------------------------+
    | Type      | Default     | Possible values          |
    +===========+=============+==========================+
    | *string*  | abort       |  abort | keep | replace  |
    +-----------+-------------+--------------------------+

------------------

``[behaviour].incorrect_checksum_action``
    Set which policies to adopt when checksum doesn't match.

    +-----------+-------------+--------------------------+
    | Type      | Default     | Possible values          |
    +===========+=============+==========================+
    | *string*  | remove       |  keep | remove          |
    +-----------+-------------+--------------------------+

index
=========

``[index].indexes``
    Set the indexes list to use for large operation.
    This parameter is used for load-balancing on several indexes, to speed up large search-API requests.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | esgf-node.ipsl.upmc.fr   |
    +-----------+--------------------------+

------------------

``[index].default_index``
    Set the index to use in priority.

    +-----------+--------------------------+
    | Type      | Default                  |
    +===========+==========================+
    | *string*  | esgf-node.ipsl.upmc.fr   |
    +-----------+--------------------------+

locale
=========

``[locale].country``
    Set the country in which synda is installed.

    +-----------+
    | Type      |
    +===========+
    | *string*  |
    +-----------+

api
=========

``[api].esgf_search_chunksize``
    Maximum files number returned by one api call.

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 9000          |
    +-----------+---------------+

------------------

``[api].esgf_search_http_timeout``
    HTTP timeout in seconds (time to wait for HTTP esgf_search api response).

    +-----------+---------------+
    | Type      | Default       |
    +===========+===============+
    | *int*     | 300           |
    +-----------+---------------+

install
=========

``[install].interactive``
    User Confirmation required before to install new files in the Database.

    +-----------+-----------+
    | Type      | Default   |
    +===========+===========+
    | *boolean* | true      |
    +-----------+-----------+
