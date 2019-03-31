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
import time
import graphviz as gv
import networkx.drawing
# from networkx.drawing.nx_pydot import grahviz_layout
# from graphviz import Digraph
import matplotlib.pyplot as plt
import random
import csv
# import pylab as plt
# import random
# import scipy
import numpy as np

# Graph the Conditional Probability Table for the rated variables
x = np.arange(1,10)
y = [0.99,0.98,0.95,0.80,0.50,0.20,0.10,0.05,0.01]
plt.subplots()
plt.plot(x,y,'-o')
plt.xlabel('Rating')
plt.ylabel('Probability of Satisfaction')
plt.grid()
plt.ylim(0,1)
plt.savefig('output/rated_prob.png')

plt.figure()
volume = [0.1,1,5,10,20,30,40,50,75,100,150]
y = [0.99,0.95,0.85,0.75,0.55,0.40,0.30,0.22,0.10,0.05,0.01]
plt.subplots()
plt.plot(volume,y,'-o')
plt.xlabel('Vehicle Volume [cubic meters]')
plt.ylabel('Probability of Satisfaction')
plt.grid()
plt.ylim(0,1)
plt.savefig('output/volume_prob.png')

plt.figure()
weight = [1,5,10,20,30,40,50,100,200]
y = [0.99,0.98,0.95,0.90,0.80,0.70,0.60,0.40,0.30]
plt.subplots()
plt.plot(weight,y,'-o')
plt.xlabel('Vehicle Mass [mt]')
plt.ylabel('Probability of Satisfaction')
plt.grid()
plt.ylim(0,1)
plt.savefig('output/weight_prob.png')

plt.figure()
crew = [5,10,15,20,30,40,50,60,80,100,150,200,400]
y = [0.01,0.08,0.15,0.20,0.3,0.4,0.5,0.6,0.72,0.8,0.9,0.95,0.99]
plt.subplots()
plt.plot(crew,y,'-o')
plt.xlabel('Crew Size')
plt.ylabel('Probability of Satisfaction')
plt.grid()
plt.ylim(0,1)
plt.savefig('output/crew_prob.png')

plt.figure()
fbd = [0.5,1,2,3,4,5,6,7,8,9,10]
y = [0.99,0.95,0.85,0.75,0.65,0.55,0.45,0.35,0.25,0.15,0.05]
plt.subplots()
plt.plot(fbd,y,'-o')
plt.xlabel('Freeboard [m]')
plt.ylabel('Probability of Satisfaction')
plt.grid()
plt.ylim(0,1)
plt.savefig('output/fbd_prob.png')

plt.show()
