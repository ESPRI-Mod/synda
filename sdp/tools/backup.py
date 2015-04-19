#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

"""This script creates a sqlite3 hot backup.

TODO
    Maybe replace this file with a shell script when minimal sqlite3 version
    supported by synda include '.backup' command.
"""    

import argparse
import sqlite3
import shutil
import time
import os

def sqlite3_hot_backup(db_file, db_backup_file):

    if not os.path.isfile(db_file):
        raise Exception("Db file not found: {}".format(db_file))
    if os.path.isfile(db_backup_file):
        raise Exception("Backup file already exist: {}".format(db_backup_file))

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('begin immediate')    # Lock database before making a backup

    # copy db file
    shutil.copyfile(db_file, db_backup_file)

    # copy journal file
    #
    # (with some sqlite3 version and on some filesystem, when running 'begin
    # immediate' command, the journal file is created)
    #
    db_journal_file=db_file+'-journal'
    db_journal_backup_file=db_backup_file+'-journal'
    #
    if os.path.isfile(db_journal_file) and not os.path.isfile(db_journal_backup_file):
        shutil.copyfile(db_journal_file, db_journal_backup_file)

    connection.rollback()                # Unlock database
    connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d','--db_file',required=True)
    parser.add_argument('-b','--db_backup_file',required=True)
    args=parser.parse_args()

    sqlite3_hot_backup(args.db_file, args.db_backup_file)
