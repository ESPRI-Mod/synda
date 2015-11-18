#!/bin/bash -e
#
# Dependencies
#  pandoc

# func

usage ()
{
    cat >&2 << EOF

USAGE: ./$(basename $0): [-c] [-f] [-h] [ MODULE ]

POSITIONAL ARGS:
   MODULE       Specify which module(s) to build
                Available modules are: 'transfer','postprocessing'.
                If no module specified, install 'transfer' module.

OPTIONS:
   -c      build archive
   -f      send archive to http server
   -h      Show this message

EOF
}

build ()
{
    module="$1"

    # obsolete
    #
    # HACK PRE-BUILD
    # (temporarily copy common libs into app's bin folder)
    #for f in bin/*; do
    #    fname=${f##*/}
    #    cp -i bin/$fname ../$module/bin
    #done

    cd ../$module
    python setup.py sdist
    cd -

    # obsolete
    #
    # HACK POST-BUILD
    # (remove copy common libs from app's bin folder)
    #for f in bin/*; do
    #    fname=${f##*/}
    #    rm ../$module/bin/$fname
    #done
}

upload ()
{
    local file_=${1}

    scp $file_ $webhost
}

get_archive_name ()
{
    local version="$1"
    local module_light_name="$2" # sdt, sdp..

    local archive_name
    local dist_dir

    archive_name=${module_light_name}-${version}.tar.gz

    dist_dir=$src_snapshot_root/${module_light_name}/dist

    echo "$dist_dir/$archive_name"
}

get_version ()
{
    local app_file="$1"

    local version

    version=$(cat $app_file | grep "version=" | sed "s/[[:alpha:]=']*//g" )

    echo $version
}

# check

if [ $# -eq 0 ]; then
    usage
    exit 0
fi

# retrieve args

deploy=0
buildpackage=0
verbose=
sdt_mod=0
sdp_mod=0
while getopts 'acfhv' OPTION
do
  case $OPTION in
  c)    buildpackage=1
        ;;
  f)    deploy=1
        ;;
  h)    usage
        exit 2
        ;;
  v)    verbose="-v"
        ;;
  ?)    exit 1 # don't forget that one, as having this option trigger special getopts incorrect option check mecanisms
        ;;
  esac
done

# remove options so to only keep positional arguments
shift $((OPTIND-1))

# retrieve positional args
if [ $# -ge 1 ]; then
    for module in "$@"; do
        if [ $module = "transfer" ]; then
            sdt_mod=1
        elif [ $module = "postprocessing" ]; then
            sdp_mod=1
        else
            usage
            exit 0
        fi
    done
else
    # default if no args

    sdt_mod=1
fi


# env. check
#if [ -z "$SYNDA_SRC_ROOT" ]; then
#    echo "Error: SYNDA_SRC_ROOT is not set"
#    exit 1
#fi
if [ -z "$SYNDA_WEBHOST" ]; then
    echo "Error: SYNDA_WEBHOST is not set"
    exit 1
fi

# init
webhost=$SYNDA_WEBHOST
#src_snapshot_root=$SYNDA_SRC_ROOT # obsolete
src_snapshot_root=$(dirname $(pwd))

# --- action --- #

# rebuild the archive
if [ "$buildpackage" = "1" ]; then

    if [ "$sdt_mod" = "1" ]; then
        build sdt
    fi

    if [ "$sdp_mod" = "1" ]; then
        build sdp
    fi
fi

# send tarball to apache
if [ "$deploy" = "1" ]; then

    if [ "$sdt_mod" = "1" ]; then
        version=$( get_version $src_snapshot_root/sdt/bin/sdapp.py )
        archive=$( get_archive_name $version sdt )
    fi

    if [ "$sdp_mod" = "1" ]; then
        version=$( get_version $src_snapshot_root/sdp/bin/spapp.py )
        archive=$( get_archive_name $version sdp )
    fi

    upload $archive
fi

exit 0
