import spconst

# this mapping means transform 'key' event into 'value' pipeline (with specified status).
event_pipeline_mapping={
    spconst.EVENT_OUTPUT12_VARIABLE_COMPLETE:      ('IPSL_VARIABLE', spconst.PPPRUN_STATUS_WAITING),
    spconst.EVENT_OUTPUT12_LATEST_DATASET_COMPLETE:('IPSL_DATASET',  spconst.PPPRUN_STATUS_PAUSE),
    spconst.EVENT_VARIABLE_COMPLETE:               ('IPSL',          spconst.PPPRUN_STATUS_WAITING),
    spconst.EVENT_CDF_VARIABLE_N:                  ('CDF_VARIABLE',  spconst.PPPRUN_STATUS_PAUSE),   # maybe use IPSL_VARIABLE here (i.e. IPSL_DATASET may be done while IPSL_VARIABLE is running..)
    spconst.EVENT_CDF_DATASET:                     ('CDF_DATASET',   spconst.PPPRUN_STATUS_PAUSE),   # called for each variable, but duplicate dataset are ignored (i.e. for some project, a dataset is a group of variable)
    spconst.EVENT_CDF_VARIABLE_O:                  ('CDF',           spconst.PPPRUN_STATUS_PAUSE)
}

# this mapping means
#  - when creating 'value pipeline', set it's status to 'waiting' if 'key pipeline' is done, else 'pause'
#  - once 'key pipeline' has ended, start 'value pipeline'
trigger={
    'CDF_VARIABLE':('CDF_DATASET',spconst.TRIGGER_TYPE_NV2D),
    'IPSL_VARIABLE':('IPSL_DATASET',spconst.TRIGGER_TYPE_NV2D),
    'IPSL_DATASET':('CDF_VARIABLE',spconst.TRIGGER_TYPE_D2NV),
    'IPSL':('CDF',spconst.TRIGGER_TYPE_D2D)
}
