# Synda FAQ

### 'Module argparse was already imported' error

Run command below

    pip uninstall argparse

### "('system library', 'fopen', 'No such file or directory')" error during certificate retrieving

unset all X509 environment variable 
remove '~/.esg' directory

### 'OpenSL: error:14094416:SSL routines:SSL3_READ_BYTES:sslv3 alert certificate unknown' error

This signals that the server does not trust the certificate issued by the MyProxy CA

You might need to re-install the set of trusted ESGF certificates:

* remove everything in the directory ~/.esg/*
* run the wget script to download a new set of trusted certificates

If this doesn't help, contact the ESGF users mailing list to notify an ESGF
administrators there might be a problem with the server certificate

More info: https://github.com/ESGF/esgf.github.io/wiki/CMIP5_FAQs

### "No module named datetime" error

Remove virtualenv from the path

    export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games

### AttributeError: 'FFILibrary' object has no attribute 'SSL_OP_NO_TICKET' error

Run command below in Synda virtualenv to retrieve pyopenssl HEAD version from github

    easy_install https://github.com/pyca/pyopenssl/tarball/master

More info: http://stackoverflow.com/questions/23006023/error-installing-pyopenssl
