
#!/bin/bash -e
synda_wo stop
sudo service sdt stop
sudo service sdp stop
sleep 8
rm -f /var/lib/synda/sdt/sdt.db
rm -f /var/lib/synda/sdp/sdp.db
rm -f /var/log/synda/sdp/*
rm -f /var/log/synda/sdt/*
cd /prodigfs/prodigfs_test/esgf/mapfiles/.
rm -fr CMIP5/*
rm -fr CORDEX/*
cd /prodigfs/prodigfs_test/esgf/mirror/.
rm -fr CMIP5/*
rm -fr CORDEX/*
cd /prodigfs/prodigfs_test/esgf/process/.
rm -fr CMIP5/*
rm -fr CORDEX/*
cd /prodigfs/prodigfs_test/project/.
rm -fr CMIP5/*
rm -fr CORDEX/*
cd
sudo service sdt start
sudo service sdp start
date > /tmp/reset.log
