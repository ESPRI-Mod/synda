#!/bin/bash -e

# Description
#   This script apply remapcon2 cdo-command on a variable,
#   creating the NetCF interpolated variable "interpolated" tree.
#   Processes by variable.
#
# Notes
#   - trailing slash is mandatory in input
#   - dependencies : cdo
#   - time to run ~> ?? mn
#
# Usage
#   ./spatial_interpolation.sh <PROJECT> <SCR_PATH> <DEST_PATH>
#
# Input
#   The project ID
#   <PROJECT>
#   An atomic dataset full path as the directory that contains NetCDF files
#   <SRC_PATH>  : /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>/
#
# Output
#   An atomic dataset full path for interpolated NetCDF
#   <DEST_PATH> : /prodigfs/project/<PROJECT>/interpolated/<downstream_DRS>/


# ------ functions ------ #

curdate ()
{
    date +'%Y/%m/%d %I:%M:%S %p'
}

msg ()
{
    l__code="${1}"
    l__msg="${2}"

    echo "$(curdate) ${l__code} ${l__msg}" 1>&2
}


# --------- arguments & initialization --------- #

while [ "${1}" != "" ]; do
    case "${1}" in
        # Project ID/Facet
        "--project")            shift; project="${1}"             ;;

        # /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>
        "--src_variable_path")  shift; process_path="${1}"        ;;

        # /prodigfs/project/<PROJECT>/interpolated/<downstream_DRS>
        "--dest_variable_path") shift; interpolated_path="${1}"   ;;
    esac
    shift
done


# --------- main --------- #

msg "INFO" "spatial_interpolation.sh started (variable_path = ${process_path})"

cat > CDF_CMIP5_grid << EOF
gridtype  = lonlat
gridsize  = 259200
xname     = lon
xlongname = longitude
xunits    = degrees_east
yname     = lat
ylongname = latitude
yunits    = degrees_north
xsize     = 720
ysize     = 360
xinc      = 0.5
yinc      = 0.5
xfirst   = -179.75
yfirst   = -89.75
EOF

umask g+w
# This is needed, because cdo expects destination path to exist (or at least parent folders in destination path).
mkdir -p ${interpolated_path}

# TODO: qsub request
for file in $(ls ${process_path}  | grep "\.nc"); do
    cdo -P 16 -O remapcon2,CDF_CMIP5_grid ${process_path}${file} ${interpolated_path}${file}
done
umask g-w

rm -f CDF_CMIP5_grid

msg "INFO" "spatial_interpolation.sh complete"
