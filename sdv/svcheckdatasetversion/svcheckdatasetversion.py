#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains user acceptance testing (UAT) routines."""

import sys
import argparse
import os
import re
import sys
import time
from fabric.api import task
from fabric.api import execute as task_exec

sys.path.append("..")

from testlib.svtestutils import fabric_run
import testlib.svtestcommon as tc

def err_raw(str):
    sys.stdout.flush()
    sys.stderr.write(str)

def err(str):
    sys.stdout.flush()
    sys.stderr.write('svcheckdatasetversion: %s\n' % str)


def run():

    task_exec(tc.configure) 
    #task_exec(restart) 

    task_exec(tc.execute_basic_command)
    task_exec(tc.check_version)

    jeutest_path = './resource'
    for n in range(10):
        num = '%02d' % (n + 1)
        check_one(jeutest_path, num)


def check_dataset_version_output_load(file_, lines):
    """ Appends to the lines array the contents of file file_ with the added
        twists that :
        - lines beginning with "Date:" have their end chopped off and
        - lines equal to "Command line:" begin a section which ends just before
          the first line that is empty or not indented.

        More precisely,
        - for each ordinary line, appends to the array tuple (n, s) where n is
          the line number and s is the contents of the line as a string with
          the final newline included,
        - for each "Date:" lines, likewise except that the string is just the
          beginning of the line ("Date:"),
        - for each "Command line:" section, likewise except that the string is
          just the first line minus the newline ("Command line:").
    """
    lnum = 1
    continuation = 0
    for line in file_:
        s = None

        if continuation:
            match = re.search('^[^ 	]', line)
            if match is not None:
                continuation = 0

        if not continuation:
            match = re.search('^(Date:)', line)
            if match is not None:
                s = match.group(1)
            else:
                match = re.search('^(Command line:)\n$', line)
                if match is not None:
                    s = match.group(1)
                    continuation = 1
                else:
                    s = line

        if s is not None:
            lines.append((lnum, s))
        lnum += 1


def check_dataset_version_outputs_compare(afn, bfn):
    """ Load and compare two files containing the output of synda check
        dataset_version and compare the latter to the former.
        Returns :
        - (0) if the files are identical
        - (1, lnum, str) if the files differ - lnum gives the line number of
          the first difference, str gives a description of the difference
        - (>1) if an error occurred
    """
    alines = []
    with open(afn, 'r') as afile:
        check_dataset_version_output_load(afile, alines)

    blines = []
    with open(bfn, 'r') as bfile:
        check_dataset_version_output_load(bfile, blines)

    idx = 0
    for idx, atuple in enumerate(alines):
        (alnum, aline) = atuple
        if idx + 1 > len(blines):
            return 1, '"%s" is shorter than "%s"' % (bfn, afn)
        (blnum, bline) = blines[idx]
        if bline != aline:
            return 1, '%s:%d is different from %s:%d' % (bfn, blnum, afn, alnum)
    if len(blines) > idx + 1:
        return 1, '"%s" is longer than "%s"' % (bfn, afn)
    return 0, '%s is identical to %s modulo possible Date: and Command line: differences' % (bfn, afn)


@task
def check_one(jeutest_path, num):
    success = 69
    pfx = 'test %s' % num
    err_raw("-------------------------------------------------------------------------------\n")
    err("%s: start" % pfx)
    in_fn = '%s/check_dataset_version-%s-in.json' % (jeutest_path, num)
    out_fn = '%s/check_dataset_version-%s-out.txt' % (jeutest_path, num)
    tmp_path = '/tmp'
    if 'TMPDIR' in os.environ and len(os.environ['TMPDIR']) != 0:
        tmp_path = os.environ['TMPDIR']
    tmp_path += '/svcheckdatasetversion'
    tmp_fn = tmp_path + '/%s-out.txt' % num
    cmd_synda = 'synda check --playback "%s" dataset_version >"%s"' % (in_fn, tmp_fn)
    cmd = '''mkdir -p -- "%s" || exit 1
%s;
true
''' % (tmp_path, cmd_synda)
    fabric_run(cmd)
    if 1:
        (differ, s) = check_dataset_version_outputs_compare(out_fn, tmp_fn)
        if differ:
            err('%s: the output of synda is NOT what it should be:' % pfx)
            err('%s:   %s' % (pfx, s))
            success = 0
        else:
            err('%s: the output of synda is what it should be:' % pfx)
            err('%s:   %s' % (pfx, s))
            success = 1
    else:
        err('%s: an error occurred while running:' % pfx)
        err(cmd.rstrip('\n'))
        success = 0

    if success:
        err('%s: pass' % pfx)
        return 1
    else:
        err('%s: FAIL' % pfx)
        raise Exception('Test %s failed' % num)
        return 0


@task
def fail():
    fabric_run('false')

@task
def check_dataset_version():
    fabric_run('synda help check')
    fabric_run('synda check --help')

# init.

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run()
