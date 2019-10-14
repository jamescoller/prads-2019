#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 2019

PRADS 2019 Code

@author: jcoller
"""
# Do float division
from __future__ import division

# Imports
# matplotlib.use('TkAgg')

import networkx as nx
import graphviz as gv
import networkx.drawing
# from networkx.drawing.nx_pydot import grahviz_layout
# from graphviz import Digraph
import matplotlib.pyplot as plt
import random
# import pylab as plt
# import random
# import scipy
import numpy as np

# Setup Networks
whole = gv.Digraph(comment='Launch and Recovery Infulence Diagram',format ='png',engine = 'dot')

simple = gv.Digraph(comment='Simple Network',format ='png',engine = 'dot')

whole.attr(ratio = "0.5")
simple.attr(ratio = "0.5")

# Simple Network
simple.node('first','System', shape = 'box')
simple.node('second','Intermediate Variables')
simple.node('third','Intermediate Satisfactions',shape = 'diamond')
simple.node('fourth','Aggregate Output',shape='hexagon')

simple.edge('first','second')
simple.edge('second','third')
simple.edge('third','fourth')

# Top Level
whole.node('host','Host Vessel', shape = 'box')
whole.node('vehicle', 'Vehicle',shape = 'box')
whole.node('system','L/R System',shape = 'box')
whole.node('env','Environment',shape = 'box')


# Host Vessel Tree
"""
whole.node('fbd_min', label="Minimum\\nFreeboard")
whole.node('size_crew', 'Crew Size')
whole.node('arr_flex', label="Arrangement\\nFlexibility")
whole.node('man_avail', label="Available\\nManning")


# Vehicle Tree
whole.node('vol',label="Vehicle\\nVolume")
whole.node('weight',label="Vehicle\\nWeight")
whole.node('var',label="Variability of\\nVehicle Type")
whole.node('flex','L/R Flexibility')
whole.node('cmplx',label="Vehicle\\nComplexity")


# System Tree
whole.node('sys_req', label="System\\nRequirements")
whole.node('imp',label="Arrangement\\nImpact")
whole.node('man_req',label="Required\\nManning")
whole.node('fbd_flex',label="Freeboard\\nFlexibility")
whole.node('rel_height',label="Relative\\nHeight")
whole.node('simplicity','Simplicity of L/R')
whole.node('rated_cap', label="Rated\\nLifting\\nCapacity")
whole.node('actual_cap',label="Actual\\nLifting\\nCapacity")

# Evironment Tree
whole.node('ss','Sea State')
whole.node('wind','Wind')
whole.node('fbd_avail',label="Available\\nFreeboard")
"""

# Satisfactions
whole.node('sat_a', label="Arrangement\\nFlexibility\\nSatisfaction", shape = 'diamond')
whole.node('sat_m', label="Manning\\nSatisfaction", shape = 'diamond')
whole.node('sat_f',label="Freeboard\\nSatisfaction", shape = 'diamond')
whole.node('sat_p',label="Performance\\nSatisfaction", shape = 'diamond')
whole.node('sat_i',label="Vehicle\\nInteroperability\\nSatisfaction", shape = 'diamond')
whole.node('sat', 'Overall Satisfaction', shape = 'hexagon')

# Draw Edges

# Host Vessel

whole.edge('host','sat_f')
whole.edge('host','sat_a')
whole.edge('host','sat_m')

whole.edge('env','sat_f')
whole.edge('env','sat_m')
whole.edge('env','sat_p')

whole.edge('system','sat_f')
whole.edge('system','sat_p')
whole.edge('system','sat_a')
whole.edge('system','sat_m')

whole.edge('vehicle','sat_a')
whole.edge('vehicle','sat_m')
whole.edge('vehicle','sat_p')
whole.edge('vehicle','sat_i')

whole.edge('sat_a','sat')
whole.edge('sat_m','sat')
whole.edge('sat_f','sat')
whole.edge('sat_i','sat')
whole.edge('sat_p','sat')

"""
whole.edge('host','arr_flex')
whole.edge('host','size_crew')
whole.edge('host','fbd_min')
whole.edge('arr_flex','sat_a')
whole.edge('size_crew','man_avail')
whole.edge('man_avail','sat_m')
whole.edge('fbd_min','sat_f')
whole.edge('sat_a','sat')
whole.edge('sat_m','sat')
whole.edge('sat_f','sat')

# Vehicle


whole.edge('vehicle','vol')
whole.edge('vehicle','weight')
whole.edge('vehicle','var')
whole.edge('vehicle','flex')
whole.edge('vehicle','cmplx')
whole.edge('vol','imp')
whole.edge('weight','man_req')
whole.edge('cmplx','man_req')
whole.edge('imp','sat_a')
whole.edge('man_req','sat_m')
whole.edge('var','sat_i')
whole.edge('flex','sat_i')
whole.edge('weight','sat_p')
whole.edge('cmplx','sat_p')
whole.edge('sat_i','sat')
whole.edge('sat_p','sat')



# System

whole.edge('system','sys_req')
whole.edge('system','fbd_flex')
whole.edge('system','rel_height')
whole.edge('system','rated_cap')
whole.edge('sys_req','imp')
whole.edge('sys_req','man_req')
whole.edge('rel_height','simplicity')
whole.edge('rated_cap','actual_cap')
whole.edge('fbd_flex','sat_f')
whole.edge('simplicity','sat_p')
whole.edge('actual_cap','sat_p')


# Environment


whole.edge('env','ss')
whole.edge('env','wind')
whole.edge('ss','man_avail')
whole.edge('ss','simplicity')
whole.edge('ss','actual_cap')
whole.edge('ss','fbd_avail')
whole.edge('wind','man_avail')
whole.edge('wind','man_req')
whole.edge('wind','simplicity')
whole.edge('wind','actual_cap')
whole.edge('fbd_avail','sat_f')
"""

# Render and Save
whole.render('output/reduced_size.gv', view=True)
simple.render('output/simple.gv', view=True)
