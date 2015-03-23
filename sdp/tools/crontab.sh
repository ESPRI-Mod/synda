#
# load with
#  $ crontab crontab_ipsl.sh
#
# use bash to run commands, no matter what /etc/passwd says
SHELL=/bin/bash
#
PATH=/usr/bin:/usr/sbin:/bin:/sbin
#
# mail any output to
MAILTO=
#
SP_TOOLS=/home/synda/sdp/tools
SP_LOG=/home/synda/sdp/log
SP_BIN=/home/synda/sdp/bin
#
4  22 * * *     . $SP_TOOLS/crontab_env.sh; $SP_TOOLS/nightly_jobs.sh >> $SP_LOG/crontab.log 2>&1

