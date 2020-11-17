# Configuration parameter reference

This document describes each parameter used in "std.conf" file to configure Synda.

### daemon.user

Set daemon user.

Type: string

Default: ""

Note: the daemon must be started by root for this parameter to work.

--------------------------------------------------------

### daemon.group

Set daemon group.

Type: string

Default: ""

Note: the daemon must be started by root for this parameter to work.

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

### module.download

If true, download files from ESGF. To use Synda in discovery or post-processing
mode only, set this parameter to false.

Type: boolean

Default: true

--------------------------------------------------------

### module.post_processing

If true, send download completion events to the post-processing module.

Type: boolean

Default: 0

--------------------------------------------------------

### module.globustransfer

If true, use Globus Transfer platform to download files.

Type: boolean

Default: 0

--------------------------------------------------------

### post_processing.host

Post-processing daemon host

Type: string

Default: localhost

--------------------------------------------------------

### post_processing.port

Post-processing daemon port

Type: int

Default: 8090

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

Possible values are: "esgf_search_api", "thredds_catalog" and "apache_default_listing".

Type: string

Default: 'esgf_search_api'

--------------------------------------------------------

### core.default_path

Override 'selection file default value' directory default path

Type: string

Default: '$HOME/sdt/conf/default' for source installation and '/etc/synda/sdt/default' for system package installation.

--------------------------------------------------------

### core.selection_path

Override selection directory default path

Type: string

Default: '$HOME/sdt/selection' for source installation and '/etc/synda/sdt/selection' for system package installation.

--------------------------------------------------------

### core.data_path

Override data directory default path

Type: string

Default: '$HOME/sdt/data' for source installation and '/srv/synda/sdt/data' for system package installation.

--------------------------------------------------------

### core.db_path

Override database default path

Type: string

Default: '$HOME/sdt/db' for source installation and '/var/lib/synda/sdt' for system package installation.

--------------------------------------------------------

### core.sandbox_path

Override sandbox directory default path

Type: string

Default: '$HOME/sdt/sandbox' for source installation and '/srv/synda/sdt/sandbox' for system package installation.

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

Set globus endpoints

Type: string

Default: /esg/config/esgf_endpoints.xml

--------------------------------------------------------

### globus.destination_endpoint

Set destination endpoint

Type: string

Default: destination#endpoint
