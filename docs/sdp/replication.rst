.. _replication-sdp:

ESGF replication
================

Introduction
************

This document describes how to implement a full ESGF replication pipeline:

.. image:: synda_replication.png
   :scale: 50%
   :alt: Basic replication pipeline
   :align: center

Synda installation
******************

See synda installation from :ref:`RPM package <rpm-install-sdt>`, :ref:`DEB package <deb-install-sdt>` or :ref:`sources <src-install-sdt>`.
Then, install Synda post-processing module from :ref:`RPM package <rpm-install-sdp>`, :ref:`DEB package <deb-install-sdp>` or :ref:`sources <src-install-sdp>`.

Create a selection file to describe which data to replicate
***********************************************************

See :ref:`the selection file section <selection-file>`

.. note::

    You can create many selection files (e.g. one per project). Selection file(s) must be stored in the "selection" folder.

Create a republication pipeline
*******************************

This republication pipeline is at least composed of 2 tasks to apply on each replicated dataset:
 - The mapfile generation,
 - The ESGF publication as replicas.

Scripts
-------

- Edit ``mapfile.sh`` that will generate mapfiles using the ```esgprep mapfile`` command-line <http://is-enes-data.github.io/esgf-prepare/>`_. The script content should like:

.. code-block:: bash

   #!/bin/bash -e

   # Description
   #   This script generates ESGF mapfile.
   #   Processes by dataset.

   # --------- arguments & initialization --------- #

   while [ "${1}" != "" ]; do
       case "${1}" in
           "--project")          shift; project="${1}"          ;;
           "--dataset_pattern")  shift; input_dataset="${1}"    ;;
       esac
       shift
   done

   ESGCET_PATH="/esg/config/esgcet/"

   # --------- main --------- #

   msg "INFO" "mapfile.sh started"

   esgprep mapfile -i ${ESGCET_PATH} -v \
                   --project ${project,,} \
                   --log \
                   --max-threads 16 \
                   --no-cleanup \
                   ${input_dataset}

   msg "INFO" "mapfile.sh complete"

- Edit ``publication.sh`` that will publish the generated mapfile as replica. The script content should like:

.. code-block:: bash

   #!/bin/bash -e

   # Description
   #   This script publishes mapfiles.
   #   Processes by dataset.

   # --------- arguments & initialization --------- #

   while [ "${1}" != "" ]; do
       case "${1}" in
           "--project")          shift; project="${1}"          ;;
           "--dataset_pattern")  shift; input_dataset="${1}"    ;;
       esac
       shift
   done

   # INI files directory
   ESGCET_PATH="/esg/config/esgcet/"
   # Indexnode hostname
   MYPROXY_HOST="esgf-node.fr"
   # myproxy-logon port
   MYPROXY_PORT="7512"
   # Publisher's openID login registered
   MYPROXY_LOGIN="xxxxxx"
   # Publisher's openID password
   MYPROXY_PASSWD="xxxxxx"

   # --------- main --------- #

   msg "INFO" "replication.sh started"

   # Loads ESGF environment
   source /etc/esg.env

   # Checkup directories and temporary files
   if [ ! -d ${ESGCET_PATH} ]; then
       msg "ERROR" "${ESGCET_PATH} does not exist. STOP." >&2
       exit 1
   fi
   if [ ! -d ${HOME}/.globus ]; then
       msg "ERROR" "${HOME}/.globus does not exist. STOP." >&2
       exit 1
   fi
   if [ -f ${HOME}/.globus/certificate-file ]; then
       msg "WARNING" "${HOME}/.globus/certificate-file already exists. Deleted." >&2
       rm -f ${HOME}/.globus/certificate-file
   fi

   # Retrieve mapfile name with an esgprep dry run
   uuid=$(uuidgen)
   esgprep mapfile -i ${ESGCET_PATH} -v \
                   --project ${project,,} \
                   --no-checksum \
                   --mapfile "{dataset_id}.${uuid}" \
                   ${input_dir} 1>&2 2> /dev/null
   mapfile_orig=$(ls /tmp/map | grep "${uuid}")
   mapfile=$(echo ${mapfile_orig} | sed "s|\.${uuid}||g")
   rm -fr /tmp/map/${mapfile_orig}

   # Gets proxy certificates for publication
   msg "INFO"  "Get ESGF certificates..."
   cat ${MYPROXY_PASSWD} | myproxy-logon -b -T -s ${MYPROXY_HOST} -p ${MYPROXY_PORT} -l ${MYPROXY_LOGIN} -o ${HOME}/.globus/certificate-file -S

   # Initialize node and controlled vocabulary
   esginitialize -c -i ${ESGCET_PATH}

   msg "INFO"  "Publishing ${mapfile} on datanode..."
   # Datanode publication
   esgpublish -i ${ESGCET_PATH} \
              --project ${project,,} \
              --thredds \
              --service fileservice \
              --set-replica \
              --map ${mapfile_dir}${mapfile}
   msg "INFO"  "Publishing ${mapfile} on indexnode..."
   #Indexnode publication
   esgpublish -i ${ESGCET_PATH} \
              --project ${project,,} \
              --publish \
              --noscan \
              --service fileservice \
              --set-replica \
              --map ${mapfile_dir}${mapfile}

   msg "INFO" "replication.sh complete"

Pipeline definition
-------------------

 - Edit the file ``${SP_HOME}/conf/pipeline/republication.py`` for source installation or ``/etc/synda/sdp/pipeline/republication.py`` for package installation. This file content must be:

.. code-block:: python

    import sppipelineutils
    import sppostprocessingutils

    def get_pipeline():
        return ppp

    name='republication'

    tasks=['mapfile','publication']

    ppp = sppostprocessingutils.build_light_pipeline(name, tasks)

- Edit the file ``${SP_HOME}/conf/pipeline/spbindings/py`` for source installation or ``/etc/synda/sdp/pipeline/spbindings.py`` for package installation. This file content must be:

.. code-block:: python

    import spconst

    # Mapping: a 'key' event into the corresponding tuple of 'value' pipeline with starting 'status'
    event_pipeline_mapping = {
        spconst.EVENT_DATASET_COMPLETE: ('republication', spconst.PPPRUN_STATUS_WAITING)
    }

File discovery
**************

Install your selection file:

.. code-block:: bash

    synda install -s <selection-file>

Or upgrade the file discovery:

.. code-block:: bash

    synda upgrade

At this point, files metadata are stored in local database and data download can begin.

Files download
**************

To start the download, in single-user installation, run command below:

.. code-block:: bash

    synda daemon start

In multi-user installation, run command below:

.. code-block:: bash

    service sdt start

Files processing
****************

To start the post-processing, in single-user installation, run command below:

.. code-block:: bash

    synda_pp daemon start

In multi-user installation, run command below:

.. code-block:: bash

    service sdp start

Then, run the worker:

.. code-block:: bash

    synda_wo --script_dir /your/scripts start