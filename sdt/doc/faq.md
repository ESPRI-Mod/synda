# Synda FAQ

### sdexception.SDException: code=SDATYPES-101,message=Path not found (/srv/synda/sdt)

Run commands below

    mkdir -p /srv/synda/sdt
    sudo wget http://dods.ipsl.jussieu.fr/jripsl/synda/patches/3.2/sdcleanup_tree.sh -O /usr/share/python/synda/sdt/bin/sdcleanup_tree.sh

--------------------------------------------------------

### ImportError: No module named sysconfig

This error occurs when installing Synda from source with an old version of
'install.sh' script (<20160215). Downloading the last version of install.sh
script should fix the problem.

--------------------------------------------------------

### 'pkg_resources.DistributionNotFound: setuptools>=1.0' error

Run command below

    sudo /usr/share/python/synda/sdt/bin/pip install setuptools==19.7

--------------------------------------------------------

### 'Module argparse was already imported' error

Run command below

    pip uninstall argparse

--------------------------------------------------------

### "('system library', 'fopen', 'No such file or directory')" error during certificate retrieving

Unset all X509 environment variables and remove '~/.esg' directory.

--------------------------------------------------------

### 'OpenSL: error:14094416:SSL routines:SSL3_READ_BYTES:sslv3 alert certificate unknown' error

This signals that the server does not trust the certificate issued by the MyProxy CA

You might need to re-install the set of trusted ESGF certificates:

* remove everything in the directory ~/.esg/*
* run the wget script to download a new set of trusted certificates

If this doesn't help, contact the ESGF users mailing list to notify an ESGF
administrators there might be a problem with the server certificate

More info: https://github.com/ESGF/esgf.github.io/wiki/CMIP5_FAQs

--------------------------------------------------------

### "No module named datetime" error

Remove virtualenv from the path

    export PATH=/usr/local/bin:/usr/bin:/bin

--------------------------------------------------------

### AttributeError: 'FFILibrary' object has no attribute 'SSL_OP_NO_TICKET' error

Run command below in Synda virtualenv to retrieve pyopenssl HEAD version from github

    easy_install https://github.com/pyca/pyopenssl/tarball/master

More info: http://stackoverflow.com/questions/23006023/error-installing-pyopenssl
