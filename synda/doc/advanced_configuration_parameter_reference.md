# Advanced configuration parameter reference

This document describes each parameter used in "internal.conf" file to configure Synda.

Note: Do not change parameter values in case of doubt

### logger.feeder_name

Default name of the 'feeder' logger.

Type: string

Default: feeder

--------------------------------------------------------

### logger.consumer_name

Default name of the 'consumer' logger.

Type: string

Default: consumer

--------------------------------------------------------

### logger.domain_name

Default name of the 'domain' logger.

Type: string

Default: domain

--------------------------------------------------------

### logger.feeder_file

Default name of the 'feeder' logger file.

Type: string

Default: discovery.log

--------------------------------------------------------

### logger.consumer_file

Default name of the 'consumer' logger file.

Type: string

Default: transfer.log

--------------------------------------------------------

### logger.domain_file

Default name of the 'domain' logger file.

Type: string

Default: domain.log

--------------------------------------------------------

### checksum.type_md5

Identifier for the md5 hash type.

Mandatory value

Type: string

Default: md5

--------------------------------------------------------

### checksum.type_sha256

Identifier for the sha256 hash type.

Mandatory value

Type: string

Default: sha256

--------------------------------------------------------

### api.esgf_search_domain_name

Domain name of the esgf_search api.

Mandatory value

Type: string

Default: IDXHOSTMARK

--------------------------------------------------------

### processes.chunksize

Maximum files number returned by one esgf_search api call.

Type: int

Default: 5000

--------------------------------------------------------

### processes.http_clients

Allowed http clients

Mandatory values

Type: string

Default: wget, urllib

--------------------------------------------------------

### processes.transfer_protocols

Allowed transfer protocols

Mandatory values

Type: string

Default: http, gridftp

--------------------------------------------------------

### processes.get_files_caching

If true, enables caching logic.

Type: boolean

Default: true

--------------------------------------------------------

### hack.projects_with_one_variable_per_dataset

Allowed transfer protocols

Type: string

Default: CORDEX, CMIP6
