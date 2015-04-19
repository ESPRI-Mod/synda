#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

"""This script creates a sqlite3 hot backup."""    

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

    shutil.copyfile(dbfile, backup_file) # Make new backup file

    connection.rollback()                # Unlock database
    connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d','--db_file',required=True)
    parser.add_argument('-b','--db_backup_file',required=True)
    args=parser.parse_args()

    sqlite3_hot_backup(args.db_file, args.db_backup_file)
