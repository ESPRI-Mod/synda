#!/bin/bash
##################################
#  @program        synchro-data
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: backup.sh 1856 2012-05-06 12:45:06Z jripsl $
#  @version        $Rev: 1856 $
#  @lastrevision   $Date: 2012-05-06 14:45:06 +0200 (Sun, 06 May 2012) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
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

if [ -z "$ST_HOME" ]; then
    echo "SDBACKUP-ERR001 - Root directory not found"
    exit 1
fi

# ------ init ------ #

DB_path="$(sdconfig -n db_folder)"
log_archive_filename=logfiles.tgz
conf_archive_filename=conffiles.tgz
selections_archive_filename="selections.tgz"
g__backup_directory="$g__backup_directories/$(date '+%Y%m%d')"

#umask u=rw,g=rw,o=r # set file permission
export LANG=C

# create backup directory

mkdir -p $g__backup_directory

# ------ main ------ #

msg "INF003" "backup.sh script started"

\cp -a $DB_path/sdt.* $g__backup_directory                                                               # backup DB
tar czf $g__backup_directory/$conf_archive_filename $ST_HOME/conf                                        # backup conf
tar czf $g__backup_directory/$log_archive_filename $ST_HOME/log/*.log                                    # backup logs
tar czf $g__backup_directory/$selections_archive_filename -- $ST_HOME/selection                          # backup selection

msg "INF004" "backup.sh script complete"
