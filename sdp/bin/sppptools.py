#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains post-processing tools.

Note
    - This script is used to query a pipeline 
      (e.g. what is the next transition),
      and to create views of a pipeline
    - Maybe move this code to 'syndac'
"""

import argparse
from sppostprocessingutils import render,view
from spexception import StateNotFoundException
import sppipeline

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('current_data_state',nargs='?')
    parser.add_argument('-l','--list',choices=['state','transition'])
    parser.add_argument('-r','--render',action='store_true')
    parser.add_argument('-v','--viewer',action='store_true')
    args = parser.parse_args()

    pipeline=sppipeline.get_pipeline('IPSL_001')

    if args.list is not None:

        if args.list=='state':
            pipeline.print_state_list()
        elif args.list =='transition':
            pipeline.print_transition_list()

    elif args.render:

        focus=[args.current_data_state] if args.current_data_state else []
        graph=render(pipeline,'Post-Processing Pipeline',focus)

        f='postprocessing.png'
        graph.draw(f, prog='dot')
        
        if args.viewer:
            view(f)
    else:
        if args.current_data_state is not None:
            try:
                pipeline.set_current_state(args.current_data_state)
                pipeline.next()
                print pipeline.get_current_state().destination
            except StateNotFoundException,e:
                print 'Data state not found (%s)'%args.current_data_state
