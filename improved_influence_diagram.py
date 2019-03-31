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

# Setup Networks
whole = gv.Digraph(comment='Launch and Recovery Infulence Diagram',format ='png',engine = 'dot')

whole.attr(ratio = "0.75")

host = gv.Digraph(comment='Launch and Recovery Infulence Diagram',format ='png',engine = 'dot')
vehicle = gv.Digraph(comment='Launch and Recovery Infulence Diagram',format ='png',engine = 'dot')
system = gv.Digraph(comment='Launch and Recovery Infulence Diagram',format ='png',engine = 'dot')
env = gv.Digraph(comment='Launch and Recovery Infulence Diagram',format ='png',engine = 'dot')

colored = gv.Digraph(comment='Launch and Recovery Infulence Diagram',format ='png',engine = 'dot')

colored.attr(ratio = "0.75")

# Top Level
whole.node('host','Host Vessel', shape = 'box')
whole.node('vehicle', 'Vehicle',shape = 'box')
whole.node('system','L/R System',shape = 'box')
whole.node('env','Environment',shape = 'box')

colored.node('host','Host Vessel', shape = 'box')
colored.node('vehicle', 'Vehicle',shape = 'box', style='filled', color='gold')
colored.node('system','L/R System',shape = 'box')
colored.node('env','Environment',shape = 'box', style='filled', color='deepskyblue')

host.node('host','Host Vessel', shape = 'box')
vehicle.node('vehicle', 'Vehicle',shape = 'box')
system.node('system','L/R System',shape = 'box')
env.node('env','Environment',shape = 'box')

# Host Vessel Tree
whole.node('fbd_min', label="Minimum\\nFreeboard")
whole.node('size_crew', 'Crew Size')
whole.node('arr_flex', label="Arrangement\\nFlexibility")
whole.node('man_avail', label="Available\\nManning")

colored.node('fbd_min', label="Minimum\\nFreeboard")
colored.node('size_crew', 'Crew Size')
colored.node('arr_flex', label="Arrangement\\nFlexibility")
colored.node('man_avail', label="Available\\nManning", style='filled', color='deepskyblue')

host.node('fbd_min', label="Minimum\\nFreeboard")
host.node('size_crew', 'Crew Size')
host.node('arr_flex', label="Arrangement\\nFlexibility")
host.node('man_avail', label="Available\\nManning")

# Vehicle Tree
whole.node('vol',label="Vehicle\\nVolume")
whole.node('weight',label="Vehicle\\nWeight")
whole.node('var',label="Variability of\\nVehicle Type")
whole.node('flex','L/R Flexibility')
whole.node('cmplx',label="Vehicle\\nComplexity")

colored.node('vol',label="Vehicle\\nVolume",  shape='doublecircle', style='filled', color='gold')
colored.node('weight',label="Vehicle\\nWeight")
colored.node('var',label="Variability of\\nVehicle Type")
colored.node('flex','L/R Flexibility')
colored.node('cmplx',label="Vehicle\\nComplexity")

vehicle.node('vol',label="Vehicle\\nVolume")
vehicle.node('weight',label="Vehicle\\nWeight")
vehicle.node('var',label="Variability of\\nVehicle Type")
vehicle.node('flex','L/R Flexibility')
vehicle.node('cmplx',label="Vehicle\\nComplexity")
vehicle.node('imp','Arrangement Impact')
vehicle.node('man_req','Required Manning')

# System Tree
whole.node('sys_req', label="System\\nRequirements")
whole.node('imp',label="Arrangement\\nImpact")
whole.node('man_req',label="Required\\nManning")
whole.node('fbd_flex',label="Freeboard\\nFlexibility")
whole.node('rel_height',label="Relative\\nHeight")
whole.node('simplicity','Simplicity of L/R')
whole.node('rated_cap', label="Rated\\nLifting\\nCapacity")
whole.node('actual_cap',label="Actual\\nLifting\\nCapacity")

colored.node('sys_req', label="System\\nRequirements")
colored.node('imp',label="Arrangement\\nImpact", style='filled', color='gold')
colored.node('man_req',label="Required\\nManning")
colored.node('fbd_flex',label="Freeboard\\nFlexibility")
colored.node('rel_height',label="Relative\\nHeight")
colored.node('simplicity','Simplicity of L/R', style='filled', color='deepskyblue')
colored.node('rated_cap', label="Rated\\nLifting\\nCapacity")
colored.node('actual_cap',label="Actual\\nLifting\\nCapacity", style='filled', color='deepskyblue')

system.node('sys_req', label="System\\nRequirements")
system.node('imp',label="Arrangement\\nImpact")
system.node('man_req',label="Required\\nManning")
system.node('fbd_flex',label="Freeboard\\nFlexibility")
system.node('rel_height',label="Relative\\nHeight")
system.node('simplicity','Simplicity of L/R')
system.node('rated_cap', label="Rated\\nLifting\\nCapacity")
system.node('actual_cap',label="Actual\\nLifting\\nCapacity")

# Evironment Tree
whole.node('ss','Sea State')
whole.node('wind','Wind')
whole.node('fbd_avail',label="Available\\nFreeboard")

colored.node('ss','Sea State', shape='doublecircle', style='filled', color='deepskyblue')
colored.node('wind','Wind')
colored.node('fbd_avail',label="Available\\nFreeboard", style='filled', color='deepskyblue')

env.node('ss','Sea State')
env.node('wind','Wind')
env.node('fbd_avail',label="Available\\nFreeboard")
env.node('man_avail', label="Available\\nManning")
env.node('man_req',label="Required\\nManning")
env.node('actual_cap',label="Actual\\nLifting\\nCapacity")
env.node('man_req','Required Manning')

# Satisfactions
whole.node('sat_a', label="Arrangement\\nFlexibility\\nSatisfaction", shape = 'diamond')
whole.node('sat_m', label="Manning\\nSatisfaction", shape = 'diamond')
whole.node('sat_f',label="Freeboard\\nSatisfaction", shape = 'diamond')
whole.node('sat_p',label="Performance\\nSatisfaction", shape = 'diamond')
whole.node('sat_i',label="Vehicle\\nInteroperability\\nSatisfaction", shape = 'diamond')
whole.node('sat', 'Overall Satisfaction', shape = 'hexagon')

colored.node('sat_a', label="Arrangement\\nFlexibility\\nSatisfaction", shape = 'diamond', style='filled', color='gold')
colored.node('sat_m', label="Manning\\nSatisfaction", shape = 'diamond', style='filled', color='deepskyblue')
colored.node('sat_f',label="Freeboard\\nSatisfaction", shape = 'diamond', style='filled', color='deepskyblue')
colored.node('sat_p',label="Performance\\nSatisfaction", shape = 'diamond', style='filled', color='deepskyblue')
colored.node('sat_i',label="Vehicle\\nInteroperability\\nSatisfaction", shape = 'diamond')
colored.node('sat', 'Overall Satisfaction', shape = 'hexagon')

host.node('sat_a', label="Arrangement\\nFlexibility\\nSatisfaction", shape = 'diamond')
host.node('sat_m', label="Manning\\nSatisfaction", shape = 'diamond')
host.node('sat_f',label="Freeboard\\nSatisfaction", shape = 'diamond')
host.node('sat', 'Overall Satisfaction', shape = 'hexagon')

vehicle.node('sat_a', label="Arrangement\\nFlexibility\\nSatisfaction", shape = 'diamond')
vehicle.node('sat_m', label="Manning\\nSatisfaction", shape = 'diamond')
vehicle.node('sat_p',label="Performance\\nSatisfaction", shape = 'diamond')
vehicle.node('sat_i',label="Vehicle\\nInteroperability\\nSatisfaction", shape = 'diamond')
vehicle.node('sat', 'Overall Satisfaction', shape = 'hexagon')

system.node('sat_a', label="Arrangement\\nFlexibility\\nSatisfaction", shape = 'diamond')
system.node('sat_m', label="Manning\\nSatisfaction", shape = 'diamond')
system.node('sat_f',label="Freeboard\\nSatisfaction", shape = 'diamond')
system.node('sat_p',label="Performance\\nSatisfaction", shape = 'diamond')
system.node('sat', 'Overall Satisfaction', shape = 'hexagon')

env.node('sat_p',label="Performance\\nSatisfaction", shape = 'diamond')
env.node('sat_m', label="Manning\\nSatisfaction", shape = 'diamond')
env.node('sat_f',label="Freeboard\\nSatisfaction", shape = 'diamond')
env.node('sat', 'Overall Satisfaction', shape = 'hexagon')

# Draw Edges

# Host Vessel
host.edge('host','arr_flex')
host.edge('host','size_crew')
host.edge('host','fbd_min')
host.edge('arr_flex','sat_a')
host.edge('size_crew','man_avail')
host.edge('man_avail','sat_m')
host.edge('fbd_min','sat_f')
host.edge('sat_a','sat')
host.edge('sat_m','sat')
host.edge('sat_f','sat')

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

colored.edge('host','arr_flex')
colored.edge('host','size_crew')
colored.edge('host','fbd_min')
colored.edge('arr_flex','sat_a')
colored.edge('size_crew','man_avail')
colored.edge('man_avail','sat_m',color='deepskyblue',style='bold')
colored.edge('fbd_min','sat_f')
colored.edge('sat_a','sat',color='gold',style='bold')
colored.edge('sat_m','sat',color='deepskyblue',style='bold')
colored.edge('sat_f','sat',color='deepskyblue',style='bold')

# Vehicle
vehicle.edge('vehicle','vol')
vehicle.edge('vehicle','weight')
vehicle.edge('vehicle','var')
vehicle.edge('vehicle','flex')
vehicle.edge('vehicle','cmplx')
vehicle.edge('vol','imp')
vehicle.edge('weight','man_req')
vehicle.edge('cmplx','man_req')
vehicle.edge('imp','sat_a')
vehicle.edge('man_req','sat_m')
vehicle.edge('var','sat_i')
vehicle.edge('flex','sat_i')
vehicle.edge('weight','sat_p')
vehicle.edge('cmplx','sat_p')
vehicle.edge('sat_a','sat')
vehicle.edge('sat_m','sat')
vehicle.edge('sat_i','sat')
vehicle.edge('sat_p','sat')

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

colored.edge('vehicle','vol',color='gold',style='bold')
colored.edge('vehicle','weight')
colored.edge('vehicle','var')
colored.edge('vehicle','flex')
colored.edge('vehicle','cmplx')
colored.edge('vol','imp',color='gold',style='bold')
colored.edge('weight','man_req')
colored.edge('cmplx','man_req')
colored.edge('imp','sat_a',color='gold',style='bold')
colored.edge('man_req','sat_m')
colored.edge('var','sat_i')
colored.edge('flex','sat_i')
colored.edge('weight','sat_p')
colored.edge('cmplx','sat_p')
colored.edge('sat_i','sat')
colored.edge('sat_p','sat',color='deepskyblue',style='bold')

# System
system.edge('system','sys_req')
system.edge('system','fbd_flex')
system.edge('system','rel_height')
system.edge('system','rated_cap')
system.edge('sys_req','imp')
system.edge('sys_req','man_req')
system.edge('rel_height','simplicity')
system.edge('rated_cap','actual_cap')
system.edge('imp','sat_a')
system.edge('fbd_flex','sat_f')
system.edge('man_req','sat_m')
system.edge('simplicity','sat_p')
system.edge('actual_cap','sat_p')
system.edge('sat_a','sat')
system.edge('sat_m','sat')
system.edge('sat_f','sat')
system.edge('sat_p','sat')

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

colored.edge('system','sys_req')
colored.edge('system','fbd_flex')
colored.edge('system','rel_height')
colored.edge('system','rated_cap')
colored.edge('sys_req','imp')
colored.edge('sys_req','man_req')
colored.edge('rel_height','simplicity')
colored.edge('rated_cap','actual_cap')
colored.edge('fbd_flex','sat_f')
colored.edge('simplicity','sat_p',color='deepskyblue',style='bold')
colored.edge('actual_cap','sat_p',color='deepskyblue',style='bold')

# Environment
env.edge('env','ss')
env.edge('env','wind')
env.edge('ss','man_avail')
env.edge('ss','man_req')
env.edge('ss','simplicity')
env.edge('ss','actual_cap')
env.edge('ss','fbd_avail')
env.edge('wind','man_avail')
env.edge('wind','man_req')
env.edge('wind','simplicity')
env.edge('wind','actual_cap')
env.edge('man_avail','sat_m')
env.edge('man_req','sat_m')
env.edge('simplicity','sat_p')
env.edge('actual_cap','sat_p')
env.edge('fbd_avail','sat_f')
env.edge('sat_m','sat')
env.edge('sat_f','sat')
env.edge('sat_p','sat')

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

colored.edge('env','ss',color='deepskyblue',style='bold')
colored.edge('env','wind')
colored.edge('ss','man_avail',color='deepskyblue',style='bold')
colored.edge('ss','simplicity',color='deepskyblue',style='bold')
colored.edge('ss','actual_cap',color='deepskyblue',style='bold')
colored.edge('ss','fbd_avail',color='deepskyblue',style='bold')
colored.edge('wind','man_avail')
colored.edge('wind','man_req')
colored.edge('wind','simplicity')
colored.edge('wind','actual_cap')
colored.edge('fbd_avail','sat_f',color='deepskyblue',style='bold')

# Render and Save
host.render('output/host_vessel_tree.gv', view=True)
vehicle.render('output/vehicle_tree.gv', view=True)
system.render('output/system_tree.gv', view=True)
env.render('output/env_tree.gv', view=True)
whole.render('output/whole_tree.gv', view=True)
colored.render('output/colored_tree.gv', view=True)
