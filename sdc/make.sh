#!/bin/bash -e
#
# Dependencies
#  pandoc

# func

usage ()
{
    cat >&2 << EOF

USAGE: $(basename $0): [-a] [-b] [-h] [ MODULE ]

POSITIONAL ARGS:
   MODULE       Specify which module(s) to build
                Available modules are: 'transfer','postprocessing'.
                If no module specified, install 'transfer' module.

OPTIONS:
   -a      send prod. archive and files to website
   -c      build archive
   -f      send dev. archive to website
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

# check

if [ $# -eq 0 ]; then
    usage
    exit 0
fi

# retrieve args

deployprod=0
deploydev=0
g__buildpackage=0
g__verbose=
g__transfer=0
g__postprocessing=0
while getopts 'acfhv' OPTION
do
  case $OPTION in
  a)    deployprod=1
        ;;
  c)    g__buildpackage=1
        ;;
  f)    deploydev=1
        ;;
  h)    usage
        exit 2
        ;;
  v)    g__verbose="-v"
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
            g__transfer=1
        elif [ $module = "postprocessing" ]; then
            g__postprocessing=1
        else
            usage
            exit 0
        fi
    done
else
    # default if no args

    g__transfer=1
fi

# init
src_snapshot_root=/home/synda/src
sdt_src=$src_snapshot_root/sdt
sdp_src=$src_snapshot_root/sdp
sdt_version_prod="2.9"
sdt_version_dev="2.9"
sdp_version_prod="1.0"
sdp_version_dev="1.0"
sdt_archive_dev=sdt-${sdt_version_dev}.tar.gz
sdp_archive_dev=sdp-${sdp_version_dev}.tar.gz
sdt_archive_prod=sdt-${sdt_version_prod}.tar.gz
sdp_archive_prod=sdp-${sdp_version_prod}.tar.gz
webhost=


# check

if [ -z "$webhost" ]; then
    echo "Error: webhost is not set"
    exit 1
fi

if ! which pandoc &>/dev/null; then
    echo "Error: pandoc not found"
    exit 1
fi


# action

# rebuild the archive
if [ "$g__buildpackage" = "1" ]; then

    if [ "$g__transfer" = "1" ]; then
        build sdt
    fi

    if [ "$g__postprocessing" = "1" ]; then
        build sdp
    fi

fi

# send the prod. package to apache
if [ "$deployprod" = "1" ]; then

    if [ "$g__transfer" = "1" ]; then
        # gen doc
        cd $sdt_src/doc
        pandoc -s USER_GUIDE -o user_guide.html
        pandoc -s UPGRADE_GUIDE -o upgrade_guide.html
        pandoc -s ADMIN_GUIDE -o admin_guide.html
        cd -
        FILES="$sdt_src/doc/TEMPLATE $sdt_src/doc/FAQ $sdt_src/doc/user_guide.html $sdt_src/doc/upgrade_guide.html $sdt_src/doc/admin_guide.html $sdt_src/doc/README $sdt_src/doc/CHANGELOG $sdt_src/doc/LICENSE $sdt_src/dist/$sdt_archive_prod"
        scp $FILES $webhost
    fi

    if [ "$g__postprocessing" = "1" ]; then
        FILES="$sdp_src/dist/$sdp_archive_prod"
        scp $FILES $webhost
    fi
fi

# send the dev. package to apache
if [ "$deploydev" = "1" ]; then
    if [ "$g__transfer" = "1" ]; then
        upload $sdt_src/dist/$sdt_archive_dev
    fi

    if [ "$g__postprocessing" = "1" ]; then
        upload $sdp_src/dist/$sdp_archive_dev
    fi
fi
