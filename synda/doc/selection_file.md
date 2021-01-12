# Selection file

A selection file contains parameters to define which data you want to download
from ESGF archive, how to download it and how to store the data.

The user defines one or many selection files. Each of them have a list of
facets (variables, frequencies, experiments, ensemble, model..). Using them,
the program explore the ESGF archive and download all the corresponding
available files. The program may be run regularly to download the possible new
files. Typically each file is associated with an analysis (cfmip, downscaling
and so on). Create as many selection files as you want in the 'selection'
folder.

Those selection files are stored in *$HOME/sdt/selection* folder (source
installation) or */etc/synda/sdt/selection* (system package installation).

Example of a selection file

    project=CMIP5
    model=CNRM-CM5 CSIRO-Mk3-6-0
    experiment=historical amip
    ensemble=r1i1p1
    variable[atmos]=tasmin tas psl
    variable[cfDay]=albisccp cltisccp pctisccp rlut rlutcs rsut rsutcs
    variable[ocean fx]=areacello sftof
    variable[land mon]=mrsos,nppRoot,nep
    variable[seaIce mon]=sic evap
    variable[ocnBgchem mon]=dissic fbddtalk
    variable[Lmon]=mrro mrso

Notes:

* many selection file examples can be found [here](https://github.com/Prodiguer/synda/tree/master/sdt/selection/sample)
* selection files are sometimes called 'template' or 'selection form'

Next parts of this document are organized in 3 main sections

* Selection file format
* Selection file parameter
* Selection file management

## Selection file format

A selection file accepts the four following line formats

### realm frequency and variable(s)

Definition

    variable[<realm>][<frequency>]=<variable1> <variable2> ...

Example

    variable[atmos][mon]=tas psl tasmin

Note

* space is used as variable delimiter

### facet(s) and variable(s)

Definition

    variable[<facet1> <facet2> <facet3> ...]=<variable1> <variable2> ...

Example

    variable[rcp26 atmos mon]=tasmin tasmax

Note

* space is used as facets and variables delimiter

### name and value

Definition

    <name>=<value>

Example

    experiment=rcp26

### standalone value

Definition

    <value>

Example

    rcp26

### Notes

* Blank line are ignored.
* Selection files may include comments, prefixed by specific characters (#).
* Trailing comments are not supported.

## Selection file parameter

See [selection file parameter reference](selection_file_parameter_reference.md)

## Selection file management

### Adding a selection file

Create a new selection file in the 'selection' folder and set the filters.

Then run command below to start the discovery

    synda install -s <selection-file>

### Editing a selection file

Edit the file and change filters accordingly.

Then run command below

    synda install -s <selection-file>

### Removing a selection file

Run command below to remove files matching the selection file

    synda remove -s <selection-file>

Then manually remove the selection file from the 'selection' folder.
