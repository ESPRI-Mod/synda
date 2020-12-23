#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains progressbar and spinning functions."""

import sys
import os
import time
import threading
import argparse
from progress.spinner import Spinner
import sdapp
import sdconfig
import sdtools
from sdexception import SDException

class ProgressThread():
    _stop_event = threading.Event()
    end_message=None
    max_message_width=100

    class MySpinnerThread(threading.Thread):
        def __init__(self,spinner,sleep,stop_event):
            threading.Thread.__init__(self)
            self.spinner=spinner
            self.sleep=sleep
            self.stop_event=stop_event

        def run(self):
            while not self.stop_event.is_set():
                self.spinner.next()
                time.sleep(self.sleep)

    @classmethod
    def stop(cls):
        cls._stop_event.set()
        cls.cleanup()

    @classmethod
    def is_message_correct(cls,msg):
        if msg is None:
            return True # message can be None
        else:
            if len(msg)>cls.max_message_width:
                return False
            else:
                return True

    @classmethod
    def start(cls,spinner_type=None,sleep=0.5,running_message='Loading ',end_message='Done.'):

        if spinner_type is None:
            spinner_type=0 if sdconfig.config.get('interface','unicode_term')=='0' else 1

        # check
        if not cls.is_message_correct(running_message):
            raise SDException('SDPROGRE-001','Incorrect message')
        if not cls.is_message_correct(end_message):
            raise SDException('SDPROGRE-002','Incorrect message')

        cls._stop_event.clear()
        cls.end_message=end_message

        if spinner_type==0:
            spinner = Spinner(running_message)
        elif spinner_type==1:
            spinner = K2KSpinner(running_message)

        spinner_thread=cls.MySpinnerThread(spinner,sleep,cls._stop_event)
        spinner_thread.setDaemon(True)
        spinner_thread.start()

    @classmethod
    def cleanup(cls):

        # erase the spinner
        space=' '*cls.max_message_width
        sys.stderr.write('\r%s\r'%space)

        # print end message if any (on spinner line)
        if cls.end_message is not None:
            sys.stderr.write('%s\n\n'%cls.end_message)

        sys.stderr.flush()
        sys.stdout.flush()

        # hack
        #
        # Something is hidding the cursor once the spinner is done, but I don't
        # know what exactly. Code below is a quickfix used to turn on the
        # cursor once spinner is done.
        #
        sdtools.set_terminal_cursor_visible()

class SDProgressDotAuto():
    default_divisor=10
    divisor=default_divisor
    dividend=0

    @classmethod
    def reset(cls,divisor=default_divisor):
        cls.dividend=0
        cls.divisor=divisor

    @classmethod
    def print_char(cls,char='.'):
        if (cls.dividend%cls.divisor)==0:
            sys.stderr.write(char)
        cls.dividend+=1

    @classmethod
    def progress_complete(cls):
        sys.stderr.write('\n')

class SDProgressDot():

    @classmethod
    def progress_begin(cls,msg=''):
        sys.stderr.write('%s'%msg)

    @classmethod
    def print_char(cls,char="."):
        sys.stderr.write(char)

    @classmethod
    def progress_complete(cls,msg=''):
        sys.stderr.write('%s\n'%msg)

class SDProgressBar():

    @classmethod
    def progress_complete(cls):
        sys.stderr.write('\n')

    @classmethod
    def print_progress_bar(cls,total,current,title='',progress_char="#"):

        # Tricky statement:
        # enumerate() based for-loop indices range is [0=>(total-1)]
        # we want this range to be [1=>total], so we add 1.
        current+=1


        if total==1:
            percent=100
        else:
            percent=(current*100)/total

        sys.stderr.write("\r%s[%-50s] %i%%"%(title,progress_char*(percent/2), percent))

class K2KSpinner():
    idx=0
    sprite=[
                u'▉            ',
                u'▊▉           ',
                u'▋▊▉          ',
                u'▌▋▊▉         ',
                u'▍▌▋▊▉        ',
                u'▎▍▌▋▊▉       ',
                u'▏▎▍▌▋▊▉      ',
                u' ▏▎▍▌▋▊▉     ',
                u'  ▏▎▍▌▋▊▉    ',
                u'   ▏▎▍▌▋▊▉   ',
                u'    ▏▎▍▌▋▊▉  ',
                u'     ▏▎▍▌▋▊▉ ',
                u'      ▏▎▍▌▋▊▉',
                u'       ▏▎▍▌▉▊',
                u'        ▏▎▉▊▋',
                u'         ▉▊▋▌',
                u'        ▉▊▋▌▍',
                u'       ▉▊▋▌▍▎',
                u'      ▉▊▋▌▍▎▏',
                u'     ▉▊▋▌▍▎▏ ',
                u'    ▉▊▋▌▍▎▏  ',
                u'   ▉▊▋▌▍▎▏   ',
                u'  ▉▊▋▌▍▎▏    ',
                u' ▉▊▋▌▍▎▏     ',
                u'▉▊▋▌▍▎▏      ',
                u'▉▋▌▍▎▏       ',
                u'▊▉▍▎▏        ',
                u'▋▊▉▏         ',
                u'▌▋▊▉         '
    ]

    def __init__(self,label):
        self.label=label

    def next(self):
        self.idx

        if self.idx == 29:
            self.idx=4

        sys.stderr.write("\r")
        sys.stderr.write(self.sprite[self.idx])

        self.idx+=1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--type',choices=['basic','K2K'],default='basic')
    args = parser.parse_args()

    if args.type == 'basic':
        ProgressThread.start(spinner_type=0,sleep=0.2)
    elif args.type == 'K2K':
        ProgressThread.start(spinner_type=1,sleep=0.1)

    time.sleep(5)

    ProgressThread.stop()
