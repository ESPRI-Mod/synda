# Selection file

To select which data to download, you need to set filters. Filters are stored
in selection files (aka template). Those selection files are stored in
'$HOME/sdt/selection' folder (single-user installation) or
'/etc/synda/sdt/selection' (multi-user installation).

Example of a selection file

    project=CMIP5
    model=CNRM-CM5 CSIRO-Mk3-6-0
    experiment=historical amip
    ensemble=r1i1p1
    variable[atmos][mon]=tasmin tas psl
    variable[ocean][fx]=areacello sftof
    variable[land][mon]=mrsos,nppRoot,nep
    variable[seaIce][mon]=sic evap
    variable[ocnBgchem][mon]=dissic fbddtalk

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
* Selection files may include comments, prefixed by specific characters (#)

## Selection file parameters

See [Selection file parameter reference](selection_file_parameter_reference.md)

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
