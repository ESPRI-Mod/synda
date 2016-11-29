#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""Contains postprocessing utils routines."""

import os
import sys
from subprocess import call
import argparse
import types
from spexception import SPException,StateNotFoundException

def increment_state_code(sta):
    nbr=int(sta[1:])
    nbr+=100
    nbr_s='%04d'%nbr
    return 'S'+nbr_s

def build_light_pipeline(pipeline_name,tasks):
    ppp=PostProcessingPipeline(pipeline_name)

    curr_state='S0100'
    dest_state='S0200'
    for i,task in enumerate(tasks):
        t=Transition(name=task,destination=dest_state)

        if i==0:
            s=State(name=curr_state,transition=t,initial=True)
        else:
            s=State(name=curr_state,transition=t)

        ppp.add(s)

        curr_state=increment_state_code(curr_state)
        dest_state=increment_state_code(dest_state)

    # add final state (with no transition attached)
    s=State(name=curr_state,transition=None)
    ppp.add(s)

    return ppp

def convert():
    #convert -delay 50 /tmp/*.png -loop 0 animated.gif
    pass

def view(file):
    VIEWER = os.environ.get('SP_IMG_VIEWER','eog')
    #li=[VIEWER, file]
    li=[VIEWER, '-f', file]
    call(li)

def render(pipeline, title=None, focus=[]):
    import pygraphviz as pgv

    graph = pgv.AGraph(title=title, **pipeline.DOT_ATTRS)
    graph.node_attr.update(State.DOT_ATTRS)


    for state in pipeline.states.values():
        if state.source in focus:
            shape = state.DOT_FOCUS
        else:
            shape = State.DOT_ATTRS['shape']
        graph.add_node(n=state.source, shape=shape)


    # this is to print edge showing where to start reading the graph (can be removed as not used)
    #graph.add_node('null', shape='plaintext', label=' ')
    #graph.add_edge('null', pipeline.init_state.source)


    for s in pipeline.states.values():
        if s.transition is not None: # this is not to print a edge when transition is None
            graph.add_edge(s.source, s.transition.destination, label=s.transition.name) # TODO: add support for dict type

    return graph

class PostProcessingPipeline(object):
    DOT_ATTRS = {
        'directed': True,
        'strict': False,
        'rankdir': 'LR',
        'ratio': '0.3'
    }

    def __init__(self,name):
        self.name = name 
        self.states = dict()
        self.init_state = None
        self.current_state=None

    def reset(self):
        """Move to the starting state."""

        self.set_current_state()

    def set_current_state(self, state_name=None):
        if state_name is None:
            self.current_state = self.init_state
        else:
            if state_name in self.states:
                self.current_state = self.states[state_name]
            else:
                raise StateNotFoundException()

    def next(self,transition_return_code):
        """Move the pipeline to the next state.

        Note
            This func is called after each transition completion.
        """
        if self.current_state.transition is None:
            # pipeline termination

            pass
        else:

            if transition_return_code is not None:

                # check
                assert isinstance(self.current_state.transition.destination, dict)
                assert transition_return_code in self.current_state.transition.destination

                state=self.current_state.transition.destination[transition_return_code]
            else:
                state=self.current_state.transition.destination

            self.current_state=self.states[state]

    def get_current_state(self):
        """TODO: make this func and set_current_state work on the same thing (i.e. str vs object)."""
        return self.current_state

    def get_transition(self):
        """Not used."""
        return self.current_state.transition.name

    def add(self,*states):
        for state in states:

            # prevent duplicate
            if state.source in self.states:
                raise SPException()

            self.states[state.source]=state

            if state.initial:
                self.init_state = state

    def all(self):
        """Not used."""
        return [(s.source, s.transition.name, s.transition.destination) for s in self.states.values()] # TODO: add support for dict type

    def get_state_list(self,li=[],state_name=None):
        """
        Return state list in order.

        Args:
            state_name: can be used to start anywhere in the pipeline

        Note
            Recursive func.
        """
        if state_name is None:
           state_name=self.init_state.source

        transition=self.states[state_name].transition
        if transition is not None:
            li.append(self.states[state_name])
            return self.get_state_list(li=li,state_name=transition.destination) # TODO: add support for dict type
        else:
            # end of recursion

            li.append(self.states[state_name])
            return li

    def print_state_list(self,state_name=None):
        li=self.get_state_list(state_name=state_name)
        state_names=[s.source for s in li]
        self.print_list(state_names)

    def print_transition_list(self,state_name=None):
        li=self.get_state_list(state_name=state_name)
        transitions=[s.transition.name for s in li if s.transition is not None] # remove last state transition (i.e. last state transition is always 'None')
        self.print_list(transitions)

    def print_list(self,li):
        print '=>'.join(li)

class Transition():
    def __init__(self,name=None,destination=None,get_args=None):
        self.name=name
        self.destination=destination # BEWARE: can be dict type or scalar type !!! TODO: change to have only dict type here !!!

        if get_args is not None:
            self.get_args=types.MethodType(get_args, self) # override get_args with custom method

    def get_args(kw):
        # Override this method to customize job arguments

        #args=dict( (k, kw[k]) for k in ['project'] ) # filter not to send all generic args
        args=kw

        return args

class State():
    DOT_ATTRS = {
        'shape': 'circle',
        'height': '1.2',
    }
    DOT_FOCUS = 'doublecircle'

    def __init__(self,name=None,transition=None,initial=False):
        self.source = name
        self.transition = transition
        self.initial = initial

    def __str__(self):
        return "%s==(%s)==>%s"%(self.source, self.transition.name, self.transition.destination)

if __name__ == '__main__':
    name='P001'
    tasks=['t1','t2','t3']
    ppp=build_light_pipeline(name,tasks)

    f='%s.png'%name
    graph=render(ppp)
    graph.draw(f, prog='dot')

    """
    if args.viewer:
        view(f)
    """
