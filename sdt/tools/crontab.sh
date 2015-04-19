#
# load with
#  $ crontab crontab.sh
#
# use bash to run commands, no matter what /etc/passwd says
SHELL=/bin/bash
#
PATH=/usr/bin:/usr/sbin:/bin:/sbin
#
# mail any output to
#MAILTO=
#
ST_HOME=/home/synda/sdt
#
4  22 * * *     . $ST_HOME/tools/crontab_env.sh; $ST_HOME/tools/nightly_jobs.sh >> $ST_HOME/log/crontab.log 2>&1
