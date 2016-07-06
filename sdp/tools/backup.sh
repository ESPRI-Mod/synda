#!/bin/bash
##################################
#  @program        synchro-data
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# Backup Synchro-data

# ------ functions ------ #

usage ()
{
	cat >&2 <<__END__

USAGE: ./backup.sh -d <path>

OPTIONS:
   -d              backup destination
__END__
}

curdate ()
{
    date '+%F %T'
}

msg ()
{
	l__code="$1"
	l__msg="$2"

	echo "$(curdate) - $l__code - $l__msg" 1>&2
}


# ------ chck ------ #

if [ $# -eq 0 ]; then
	usage
	exit 2
fi

# ------ args ------ #

while getopts 'd:h' OPTION
do
  case $OPTION in
  d)	g__backup_directories=$OPTARG
		;;
  h)	g__action=help
  		usage
		exit 2
		;;
  ?)	exit 1 # we come here when a required option argument is missing (bash getopts mecanism)
		;;
  esac
done

# ------ check ------ #

if [ -z "$SP_HOME" ]; then
    echo "SPBACKUP-ERR001 - Root directory not found"
    exit 1
fi

# ------ init ------ #

sqlite_backup_script="$SP_HOME/tools/backup.py"
DB_path="$(spconfig -n db_folder)"
log_archive_filename=logfiles.tgz
conf_archive_filename=conffiles.tgz
g__backup_directory="$g__backup_directories/$(date '+%Y%m%d')/sdp"

#
#umask u=rw,g=rw,o=r # set file permission
export LANG=C

# create backup directory

mkdir -p $g__backup_directory

# ------ main ------ #

msg "INF003" "backup.sh script started"

$sqlite_backup_script -d $DB_path/sdp.db -b $g__backup_directory/sdp.db                                  # backup DB
tar czf $g__backup_directory/$conf_archive_filename $SP_HOME/conf                                        # backup conf
tar czf $g__backup_directory/$log_archive_filename $SP_HOME/log/*.log                                    # backup logs

msg "INF004" "backup.sh script complete"
