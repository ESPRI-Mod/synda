import spconst

# Mapping: a 'key' event into the corresponding tuple of 'value' pipeline with starting 'status'
event_pipeline_mapping = {
    spconst.EVENT_OUTPUT12_VARIABLE_COMPLETE:       ( 'IPSL_VARIABLE',    spconst.PPPRUN_STATUS_WAITING),
    spconst.EVENT_OUTPUT12_LATEST_DATASET_COMPLETE: ( 'IPSL_DATASET',     spconst.PPPRUN_STATUS_PAUSE),
    spconst.EVENT_VARIABLE_COMPLETE:                ( 'IPSL',             spconst.PPPRUN_STATUS_WAITING),
    spconst.EVENT_CDF_INT_VARIABLE_N:               ( 'CDF_INT_VARIABLE', spconst.PPPRUN_STATUS_PAUSE),
    spconst.EVENT_CDF_INT_DATASET:                  ( 'CDF_INT_DATASET',  spconst.PPPRUN_STATUS_PAUSE),
    spconst.EVENT_CDF_INT_VARIABLE_O:               ( 'CDF_INT',          spconst.PPPRUN_STATUS_PAUSE),
    spconst.EVENT_CDF_COR_VARIABLE_N:               ( 'CDF_COR_VARIABLE', spconst.PPPRUN_STATUS_PAUSE),
    spconst.EVENT_CDF_COR_DATASET:                  ( 'CDF_COR_DATASET',  spconst.PPPRUN_STATUS_PAUSE),
    spconst.EVENT_CDF_COR_VARIABLE_O:               ( 'CDF_COR',          spconst.PPPRUN_STATUS_PAUSE)
}
# Maybe IPSL_DATASET may be done while IPSL_VARIABLE is running to trigger CDF_VARIABLE in parallel...

# Mapping: when a 'key' pipeline has ended, start the corresponding 'value' pipeline
# This means to change the status of the 'value' pipeline from 'pause' to 'waiting'
# when the 'key' pipeline reach the 'done' status
trigger = {
   'IPSL_VARIABLE': ('IPSL_DATASET', spconst.TRIGGER_TYPE_NV2D),
   'IPSL_DATASET': ('CDF_INT_VARIABLE', spconst.TRIGGER_TYPE_D2NV),
   'CDF_INT_VARIABLE': ('CDF_INT_DATASET', spconst.TRIGGER_TYPE_NV2D),
   'CDF_INT_DATASET': ('CDF_COR_VARIABLE', spconst.TRIGGER_TYPE_D2NV),
   'CDF_COR_VARIABLE': ('CDF_COR_DATASET', spconst.TRIGGER_TYPE_NV2D),
   'IPSL': ('CDF_INT', spconst.TRIGGER_TYPE_D2D),
   'CDF_INT': ('CDF_COR', spconst.TRIGGER_TYPE_D2D)
}
