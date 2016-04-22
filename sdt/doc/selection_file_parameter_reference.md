# Selection file parameter reference

This document describes each parameter used in a selection file.

## Search-api parameter

Those parameters are described [here](https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API)

## Synda parameter

Those parameters are specific to Synda and cannot be used directly with the Search-api.

This section contains the following sub-groups:

* Synda formatting parameter
* Synda local search parameter
* Synda remote search parameter
* Synda meta parameter

### Synda formatting parameter

#### local_path_format

Set daemon group.

Type: string

Default: ""

--------------------------------------------------------

#### local_path_product_format

Set daemon group.

Type: string

Default: ""

--------------------------------------------------------

#### local_path_project_format

Set daemon group.

Type: string

Default: ""

--------------------------------------------------------

#### local_path_drs_template

Set daemon group.

Type: string

Default: ""

### Synda local search parameter

#### local_path

This parameter select local files using local path.

Type: string

Default: ""

--------------------------------------------------------

#### error_msg

This parameter select local files using error message.

Type: string

Default: ""

--------------------------------------------------------

#### insertion_group_id

This parameter select local files using insertion group identifier.

Type: string

Default: ""

--------------------------------------------------------

#### status

This parameter select local files using download status.

Type: string

Default: ""

--------------------------------------------------------

#### sdget_status

This parameter select local files using sdget_status.

Type: string

Default: ""

### Synda remote search parameter

#### timeslice

This parameter select files using filename timestamp.

Type: string

Default: ""

--------------------------------------------------------

### Synda meta parameter

#### protocol

Select which protocol to use to download the data. Currently, the two supported
protocols are http and gridftp.

Type: string

Default: "http"

--------------------------------------------------------

#### searchapi_host

Set daemon group.

Type: string

Default: ""

--------------------------------------------------------

#### priority

Set download priority.

Type: integer

Default: 1000
