.. _pipeline-file:

Pipeline creation
=================

Pipeline definition file
************************

A "synda pipeline" is defined with a Python script that describe each transition to operate by the worker along the pipeline.
A "transition" is a post-process to apply to a dataset and is defined by its name, its source and destination states.

.. warning::

    The transition name has to be the same as the script you want to apply as post-process.
    For instance, in the case your post-process consist in executing the script ``copy.sh`` to each dataset the corresponding transition name is ``copy``.

We will define a pipeline called "my_pipeline" composed of 3 tasks (task_A, task_B, task_C), which will run sequentially one after the other.

Edit the file ``${SP_HOME}/conf/pipeline/my_pipeline.py`` for source installation or ``/etc/synda/sdp/pipeline/my_pipeline.py`` for package installation. This file content must be:

.. code-block:: python

    import sppipelineutils
    import sppostprocessingutils

    def get_pipeline():
        return ppp

    name='my_pipeline'

    tasks=['task_A','task_B','task_C']

    ppp = sppostprocessingutils.build_light_pipeline(name, tasks)


Binding file
************

Synda post-processing pipelines relies on "events" send by ``sdt`` to ``sdp`` module. To configure which event leads to which pipeline, we binds events and pipelines through a Python dictionary.

The binding file is used to bind events to pipelines. When a dataset, a variable or a file is downloaded by ``sdt`` an "event" can be sent to create a new post-processing entry in ``sdp.db``.

.. note::

    Only the following events can be binds to pipelines:
     - ``EVENT_FILE_COMPLETE``: the pipeline is triggered when a file is downloaded.
     - ``EVENT_VARIABLE_COMPLETE``: the pipeline is triggered when all files of a variable are downloaded.
     - ``EVENT_DATASET_COMPLETE``: the pipeline is triggered when all files of a dataset are downloaded.
     - ``EVENT_DATASET_LATEST``: the pipeline is triggered when a dataset is promoted latest.
     - ``EVENT_LATEST_DATASET_COMPLETE``: the pipeline triggered when all files of a dataset are downloaded and the dataset is promoted latest.
     - ``EVENT_NON_LATEST_DATASET_COMPLETE``: the pipeline triggered when all files of a dataset are downloaded and the dataset is not latest.

    Other events exists to deal with CMIP5-like project without considering the product facet:
     - ``EVENT_OUTPUT12_VARIABLE_COMPLETE``
     - ``EVENT_OUTPUT12_DATASET_COMPLETE``
     - ``EVENT_OUTPUT12_LATEST_DATASET_COMPLETE``
     - ``EVENT_OUTPUT12_NON_LATEST_DATASET_COMPLETE``
     - ``EVENT_OUTPUT12_DATASET_LATEST``

Edit the file ``${SP_HOME}/conf/pipeline/spbindings/py`` for source installation or ``/etc/synda/sdp/pipeline/spbindings.py`` for package installation. This file content must be:

.. code-block:: python

    import spconst

    # Mapping: a 'key' event into the corresponding tuple of 'value' pipeline with starting 'status'
    event_pipeline_mapping = {
        spconst.EVENT_VARIABLE_COMPLETE: ('my_pipeline', spconst.PPPRUN_STATUS_WAITING)
    }

Pipeline triggering
*******************

The binding file is also used to trigger pipelines between each other.
It could be useful to separate post-processing that to be apply at different DRS level (e.g., variable vs. dataset level).

For instance, we defined another pipeline called ``my_pipeline_2`` composed of tasks at the dataset level. We want that this pipeline is triggerred when all the variable of a dataset have been processed.

Edit the file ``${SP_HOME}/conf/pipeline/spbindings/py`` for source installation or ``/etc/synda/sdp/pipeline/spbindings.py`` for package installation. Add the content:

.. code-block:: python

    # Mapping: when a 'key' pipeline has ended, start the corresponding 'value' pipeline
    # This means to change the status of the 'value' pipeline from 'pause' to 'waiting'
    # when the 'key' pipeline reach the 'done' status
    trigger = {
       'my_pipeline': ('my_pipeline2', spconst.TRIGGER_TYPE_NV2D)
    }

.. note::

    Only the following triggers are supported:
     - ``TRIGGER_TYPE_NV2D``: N "variable pipeline" trigger "dataset pipeline"
     - ``TRIGGER_TYPE_V2V``: "variable pipeline" triggers "variable pipeline"
     - ``TRIGGER_TYPE_D2D``: "dataset pipeline" triggers "dataset pipeline"
     - ``TRIGGER_TYPE_D2NV``: "dataset pipeline" triggers N "variable pipeline"
