# Synda FAQ

### required = {'jpeg', 'zlib'} - SyntaxError: invalid syntax

Full error stack

    Collecting pillow>=2.4.0 (from reportlab)
      Using cached Pillow-4.0.0.tar.gz
        Complete output from command python setup.py egg_info:
        Traceback (most recent call last):
          File "<string>", line 1, in <module>
          File "/tmp/root/pip-build-525vF6/pillow/setup.py", line 138
            required = {'jpeg', 'zlib'}
                              ^
        SyntaxError: invalid syntax

This bug affects 3.6 version installed from source (RPM 3.6 and DEB 3.6 should
not be affected). It has been fixed in 3.7.

It can be fixed in 3.6 by downgrading the pypi pillow package

    pip install pillow==3.4.2

### NoSectionError: No section: 'esgf_credential'

Run commands below

    sudo sed -i -e "s/install/get','install/" /usr/share/python/synda/sdt/bin/sdconst.py 

--------------------------------------------------------

### urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)

Run commands below

    synda certificate renew -x

--------------------------------------------------------

### sdexception.SDException: code=SDATYPES-101,message=Path not found (/srv/synda/sdt)

Run commands below

    mkdir -p /srv/synda/sdt
    sudo wget http://sd-104052.dedibox.fr/synda/patches/3.2/sdcleanup_tree.sh -O /usr/share/python/synda/sdt/bin/sdcleanup_tree.sh

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

### 'OpenSL: error:SSL routines:SSL3_READ_BYTES:sslv3 alert certificate unknown' error

This signals that the server does not trust the certificate issued by the
MyProxy CA.

Run commands below

    synda certificate renew -x

If this doesn't help, you can find more info
[here](https://github.com/ESGF/esgf.github.io/wiki/CMIP5_FAQs)

--------------------------------------------------------

### "No module named datetime" error

Remove virtualenv from the path

    export PATH=/usr/local/bin:/usr/bin:/bin

--------------------------------------------------------

### AttributeError: 'FFILibrary' object has no attribute 'SSL_OP_NO_TICKET' error

Run command below in Synda virtualenv to retrieve pyopenssl HEAD version from github

    easy_install https://github.com/pyca/pyopenssl/tarball/master

More info: http://stackoverflow.com/questions/23006023/error-installing-pyopenssl
