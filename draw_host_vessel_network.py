#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 2019

PRADS 2019 Code

Recreation of Jackson Wireman's Influence Diagram for shipboard AUV L/R

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

# Setup Network
whole = gv.Digraph(comment='Launch and Recovery Infulence Diagram',format ='png',engine = 'dot')

# Top Level
whole.node('host','Host Vessel', shape = 'box')
whole.node('vehicle', 'Vehicle',shape = 'box')
whole.node('system','L/R System',shape = 'box')
whole.node('env','Environment',shape = 'box')

# Host Vessel Tree
whole.node('fbd_min', 'Minimum Freeboard')
whole.node('size_crew', 'Crew Size')
whole.node('arr_flex', 'Arrangement Flexibility')
whole.node('man_avail', 'Available Manning')

# Vehicle Tree
whole.node('vol','Vehicle Volume')
whole.node('weight','Vehicle Weight')
whole.node('var','Variability of Vehicle Type')
whole.node('flex','L/R Flexibility')
whole.node('cmplx','Vehicle Complexity')

# System Tree
whole.node('sys_req', 'System Requirements')
whole.node('imp','Arrangement Impact')
whole.node('man_req','Required Manning')
whole.node('fbd_flex','Freeboard Flexibility')
whole.node('rel_height','Relative Height')
whole.node('simplicity','Simplicity of L/R')
whole.node('rated_cap', 'Rated Lifting Capacity')
whole.node('actual_cap','Actual Lifting Capacity')

# Evironment Tree
whole.node('ss','Sea State')
whole.node('wind','Wind')

# Satisfactions
whole.node('sat_a', 'Arrangement Flexibility Satisfaction', shape = 'diamond')
whole.node('sat_m', 'Manning Satisfaction', shape = 'diamond')
whole.node('sat_f','Freeboard Satisfaction', shape = 'diamond')
whole.node('sat_p','Performance Satisfaction', shape = 'diamond')
whole.node('sat_i','Vehicle Interoperability Satisfaction', shape = 'diamond')
whole.node('sat', 'Overall Satisfaction', shape = 'hexagon')

# Draw Edges
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

whole.render('output/host_vessel_tree.gv', view=True)
