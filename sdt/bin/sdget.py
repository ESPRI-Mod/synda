#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains data file download routines.

Note
    This module contains two implementations to download data file
        - Pure python implementation (https and urllib2)
        - 'wget' based implementation
"""

import urllib2
import httplib
from os.path import expanduser, join
import sdapp
import sdconfig
from sdtools import print_stderr

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    """HTTP handler that transmits an X509 certificate as part of the request."""
    def __init__(self, key, cert):
            urllib2.HTTPSHandler.__init__(self)
            self.key = key
            self.cert = cert
    def https_open(self, req):
            return self.do_open(self.getConnection, req)
    def getConnection(self, host, timeout=300):
            return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)

def download(url, toDirectory="/tmp"):
    """Function to download a single file from ESGF."""
    
    # setup HTTP handler
    certFile = expanduser(ESGF_CREDENTIALS)
    opener = urllib2.build_opener(HTTPSClientAuthHandler(certFile,certFile))
    opener.add_handler(urllib2.HTTPCookieProcessor())
    
    # download file
    localFilePath = join(toDirectory,url.split('/')[-1])
    localFile=open( localFilePath, 'w')
    webFile=opener.open(url)

    # TODO
    # JRA: modify below to add checksum & huge file support (i.e. file that doesn't fit in memory)
    #https://gist.github.com/brianewing/994303
    #http://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file

    localFile.write(webFile.read())
    
    # cleanup
    localFile.close()
    webFile.close()
    opener.close()

def test_access():
    urlfile = urllib2.urlopen("http://www.google.com")

    data_list = []
    chunk = 4096
    while 1:
        data = urlfile.read(chunk)
        if not data:
            break
        data_list.append(data)
        #print "Read %s bytes"%len(data)

def download_with_wget(url):
    import os, sdutils

    tmpfile='/tmp/sdt_test_file.nc'

    if os.path.isfile(tmpfile):
        os.remove(tmpfile)

    (sdget_status,stdout,stderr)=sdutils.get_status_output([sdconfig.data_download_script,'-d 3',url,tmpfile],shell=False)

    print_stderr(stdout) # TODO: do not mix stderr and stdout upside down

    #print "'sdget.sh' exit code: %i"%sdget_status

    """
    if sdget_status==0:
        print 'file location: %s'%tmpfile
    """

# init.

ESGF_CREDENTIALS = "~/.esg/credentials.pem"
