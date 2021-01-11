# Configuration parameter reference

This document describes each parameter used in "std.conf" file to configure Synda.

### daemon.user

Deprecated

--------------------------------------------------------

### daemon.group

Deprecated

--------------------------------------------------------

### download.max_parallel_download

Set the number of parallel download.

Type: int

Default: 8

--------------------------------------------------------

### download.hpss

Gives HPSS service some time to move data from tape to disk.

Type: boolean

Default: 1

--------------------------------------------------------

### download.http_fallback

If true, if gridftp transfer fails, gridftp url is automatically replaced with
http url.

Type: boolean

Default: false

--------------------------------------------------------

### download.direct_http_timeout (NEW)

Direct download HTTP timeout, in seconds (time to wait for HTTP response).

Type: int

Default: 30

(sdconst.DIRECT_DOWNLOAD_HTTP_TIMEOUT is predicated)

--------------------------------------------------------

### download.async_http_timeout (NEW)

Asynchronous download HTTP timeout, in seconds (time to wait for HTTP response).

Type: int

Default: 120

(sdconst.ASYNC_DOWNLOAD_HTTP_TIMEOUT is predicated)

--------------------------------------------------------

### download.direct_db_timeout (NEW)

Used only for direct downloads
This timeout parameter specifies how long, in seconds, the connection should wait for the lock to go away until raising an exception.

Type: int

Default: 120

--------------------------------------------------------

### download.async_db_timeout (NEW)

Used only for asynchronous downloads
This timeout parameter specifies how long, in seconds, the connection should wait for the lock to go away until raising an exception.

Type: int

Default: 12000

--------------------------------------------------------

### module.download

If true, download files from ESGF. To use Synda in discovery or post-processing
mode only, set this parameter to false.

Type: boolean

Default: true

--------------------------------------------------------

### module.post_processing

Deprecated

--------------------------------------------------------

### module.globustransfer

Deprecated

--------------------------------------------------------

### post_processing.host

Deprecated

--------------------------------------------------------

### post_processing.port

Deprecated

--------------------------------------------------------

### log.verbosity_level

Log verbosity level

Type: string

Default: info

--------------------------------------------------------

### log.scheduler_profiling

If true, log code profiling information

Type: boolean

Default: 0

--------------------------------------------------------

### core.security_dir_mode

Set the location of X509 certificates.

Possible values are: "tmp", "tmpuid", "home" and "mixed".

"tmp": all users certificates are stored in Synda tmp folder.

"tmpuid": interactive user and daemon user certificates are stored into
separate subfolders (named after the user UID) inside Synda tmp folder.

"home": interactive user and daemon user certificates are stored in user home
directory.

"mixed": daemon user certificates is stored in Synda tmp folder and interactive
user certificate is stored in user home directory.

Type: string

Default: 'tmpuid'

--------------------------------------------------------

### core.metadata_server_type

Type of metadata server

Only one possible value at the moment.

Type: string

Default: 'esgf_search_api'

--------------------------------------------------------

### core.default_path

Override 'selection file default value' directory default path

Type: string

Default: '$ST_HOME/conf/default'

--------------------------------------------------------

### core.selection_path

Override selection directory default path

Type: string

Default: '$ST_HOME/selection'

--------------------------------------------------------

### core.data_path

Override data directory default path

Type: string

Default: '$ST_HOME/data'

--------------------------------------------------------

### core.db_path

Override database default path

Type: string

Default: '$ST_HOME/sdt/db'

--------------------------------------------------------

### core.sandbox_path

Override sandbox directory default path

Type: string

Default: '$ST_HOME/sandbox'

--------------------------------------------------------

### interface.unicode_term

If true, use unicode characters for progress bar.

Type: boolean

Default: 0

--------------------------------------------------------

### interface.progress

If true, show progress bar for time consuming task.

Type: boolean

Default: 0

--------------------------------------------------------

### interface.default_listing_size

This parameter drives how many results are displayed by default for "search",
"list" and "dump" subcommands.

Possible values are: "small", "medium" and "big".

Type: string

Default: small

--------------------------------------------------------

### interface.dump_listing_limit_for_small_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'small'.

Type: int

Default: 50

--------------------------------------------------------

### interface.dump_listing_limit_for_medium_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'medium'.

Type: int

Default: 100

--------------------------------------------------------

### interface.dump_listing_limit_for_big_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'big'.

Type: int

Default: 6000

--------------------------------------------------------

### interface.list_listing_limit_for_small_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'small'.

Type: int

Default: 20

--------------------------------------------------------

### interface.list_listing_limit_for_medium_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'medium'.

Type: int

Default: 200

--------------------------------------------------------

### interface.list_listing_limit_for_big_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'big'.

Type: int

Default: 20000

--------------------------------------------------------

### interface.search_listing_limit_for_small_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'small'.

Type: int

Default: 100

--------------------------------------------------------

### interface.search_listing_limit_for_medium_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'medium'.

Type: int

Default: 1000

--------------------------------------------------------

### interface.search_listing_limit_for_big_mode (NEW)

Set the total number of returned results when default_listing_size is set to 'big'.

Type: int

Default: 6000

--------------------------------------------------------

### interface.show_advanced_options (NEW)

Available for the following subcommands : count, install, search, stat, upgrade

When True allows to access the two following arguments : --timestamp_left_boundary and --timestamp_right_boundary

Example

    $ synda count -s selection.txt --timestamp_left_boundary 2012-01-01T01:00:00Z --timestamp_right_boundary 2015-01-01T01:00:00Z

Type: boolean

Default: false

--------------------------------------------------------

### behaviour.onemgf

Improve search performance (experimental).

Type: boolean

Default: false

--------------------------------------------------------

### behaviour.check_parameter

If true, perform parameter typo detection (name and value).

Example

If behaviour.check_parameter is true,

    $ synda search cmip5 taz

will raises an exception and inform the user that 'taz' value is not found.

Type: boolean

Default: 0

--------------------------------------------------------

### behaviour.ignorecase

If true, automatically fix incorrect case

Example

    $ synda search MOHC-HADGEM3-RA

This command normally raises an exception as the correct case should be 'MOHC-HadGEM3-RA'.

But if behaviour.ignorecase is true, the model name will be automatically corrected and no exception will occur.

Type: boolean

Default: true

--------------------------------------------------------

### behaviour.nearest

If true, automatically select the nearest file replica

Type: boolean

Default: false

--------------------------------------------------------

### behaviour.nearest_mode

Set nearest replica algorithm.

Possible values are: "geolocation" and "rtt".

Type: string

Default: geolocation

--------------------------------------------------------

### behaviour.lfae_mode

Set which policies to adopt when a download starts and local file already
exists ('lfae' means 'Local File Already Exist). Possible values are: "keep",
"replace" and "abort". When set to "keep", local file is used instead of the
remote file. When set to "replace", the remote file overwrites the local file.
When set to "abort", the transfer is cancelled (the transfer status is set to
'error') and the local file is kept.

Type: string

Default: abort

--------------------------------------------------------

### behaviour.incorrect_checksum_action

Set which policies to adopt when checksum doesn't match

Possible values are: "remove" and "keep"

"remove": set transfer status to error and remove the downloaded file

"keep": set transfer status to done, log a warning and keep the downloaded file

Type: string

Default: remove

--------------------------------------------------------

### index.indexes

Set the indexes list to use for large operation

Type: string

Default: pcmdi.llnl.gov

Note: this parameter is used for load-balancing on several indexes, to speed up large search-API requests

--------------------------------------------------------

### index.default_index

Set the index to use in priority

Type: string

Default: pcmdi.llnl.gov

--------------------------------------------------------

### locale.country

Set the country in which synda is installed

Type: string

Default: ""

Note: used to compute nearest replicat when "geolocation" mode is used

--------------------------------------------------------

### globus.esgf_endpoints

Deprecated

--------------------------------------------------------

### globus.destination_endpoint

Deprecated


--------------------------------------------------------

### api.esgf_search_chunksize (NEW)

Maximum files number returned by one api call.

Type: int

Default: 9000

--------------------------------------------------------

### api.esgf_search_http_timeout (NEW)

HTTP timeout in seconds (time to wait for HTTP esgf_search api response)

Type: int

Default: 300
