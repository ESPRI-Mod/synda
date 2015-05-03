# *sd28to29* command user guide

sd28to29 - upgrade synda from 2.8 to 2.9

## Synopsis

    sd28to29 -d DBFILE_28

## Usage

* Install synda 2.9 from scratch

* Move to bin directory

    cd $ST_HOME/bin

* Run upgrade script over the 2.8 database file.

    ./sd28to29 -d DBFILE_28

* Now, the new 2.9 database file should be populated with previous version data. If everything went fine, the command below will list your data from the 2.9 database.

    ./synda search -l

* Copy selection files from 2.8 selection folder to 2.9 selection folder.

* Copy parameter from 2.8 configuration file (sdt.conf) to 2.9 configuration file (sdt.conf).
