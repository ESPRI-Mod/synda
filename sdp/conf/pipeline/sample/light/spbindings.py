import spconst

# this mapping means transform 'key' event into 'value' pipeline (with specified status).
event_pipeline_mapping={
    spconst.EVENT_VARIABLE_COMPLETE:               ('P001',          spconst.PPPRUN_STATUS_WAITING)
}

# this mapping means
#  - when creating 'value pipeline', set it's status to 'waiting' if 'key pipeline' is done, else 'pause'
#  - once 'key pipeline' has ended, start 'value pipeline'
trigger={}
