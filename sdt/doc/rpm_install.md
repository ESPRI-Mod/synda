

EPEL must be installed if not already
e.g. for RHEL7, do
sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y

Install synda using

sudo yum install http://dods.ipsl.jussieu.fr/jripsl/synda/rpm/rhel7/ -y

Then edit /etc/synda/sdt/credentials.conf to set ESGF openid and password.

Note: to download file from ESGF, you need to create an openID account on one
ESGF identity provider website (e.g. PCMDI, BADC or DKRZ) and subscribe to
CMIP5-RESEARCH role.
