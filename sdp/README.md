# Synda Post-Processing module

Synda Post-Processing module is used to transform ESGF data files.

## Architecture description

Pipeline, Jobs and Workers

In the centre is a pipeline database that list individual jobs to be run. These jobs are
claimed and processed by Workers - autonomous processes that are running on the
compute farm and connect to the pipeline database to report about the progress
of Jobs or claim some more. When a Worker discovers that its predefined time is
up or that there are no more Jobs to do, it claims no more Jobs and exits the
compute farm freeing the resources.

## Version

* Stable: 1.2

* Testing: 1.3
