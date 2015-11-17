#!/bin/bash -e

# Description
#   This script apply cdscan cdat-command on a variable,
#   creating xml aggregation for every variable existing in 'process' tree.
#
# Notes
#   - CMIP5 project only
#   - trailing slash is mandatory in input
#   - python dependencies : cdat or cdat_lite
#   - time to run ~> ?? mn
#
# Requirement
#  curl (curl 7.20.1) must be installed in /usr/local
#
# Usage
#   ./cdscan.sh <path>
#
# Input
#   variable full path (e.g. <PREFIX>/esg/CMIP5/process/MIROC/MIROC-ESM/historicalNat/mon/atmos/Amon/r1i1p1/v20120710/clt/)
#
# Output
#   xml aggregation file (e.g. <PREFIX>/esg/xml/CMIP5/historicalNat/atmos/mon/ta/cmip5.MIROC-ESM.historicalNat.r1i1p1.mon.atmos.Amon.ta.latest.xml)
#
# TODO
#   None


# --------- func --------- #

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

while [ "$1" != "" ]; do
    case "$1" in
        "--project")       shift; project="$1"         ;;
        "--variable_path") shift; variable_path="$1"   ;;
    esac
    shift
done

xml_output=$( echo ${variable_path} | awk -F '/' '{print tolower($4)"."$7"."$8"."$12"."$9"."$10"."$11"."$14"."$13".xml"}' )
dir_out=$( echo ${variable_path} | awk -F '/' '{print "/prodigfs/esg/xml/"$4"/"$8"/"$10"/"$9"/"$14}' )

export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# --------- main --------- #

msg "INFO" "cdscan.sh started (variable_path = ${variable_path})"

umask g+w
mkdir -p ${dir_out}
cdscan -x ${dir_out}/${xml_output} ${variable_path}*.nc 1>&2
umask g-w

msg "INFO" "cdscan.sh complete"
