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

from Calculate_Network import Host_Ship
from Calculate_Network import Vehicle
from Calculate_Network import LR_system
from Calculate_Network import Environment
from Calculate_Network import Simulation

# Define Inputs for Baseline

# Ship: (self,name,arr_flex,size_crew,fbd_min)
ship = Host_Ship('Example Ship',3,100,1)

# System: (self,name,req,fbd_flex,rel_height,cap)
Crane1 = LR_system('Crane 1',2,2,2,20)
Crane2 = LR_system('Crane 2',4,4,4,40)

# Environment: (self,name,ss,wind)
ss2 = Environment('SS2',2,2)
ss4 = Environment('SS4',4,4)
ss6 = Environment('SS6',6,6)

# Vehicle: (self,name,volume,weight,variability,flexibility,complexity)
veh1 = Vehicle('UUV',0.5,0.1,2,2,4)
veh2 = Vehicle('MRHIB',10,5,4,3,2)
veh3 = Vehicle('HRHIB',15,10,4,5,4)

# Set up Variable Vectors
sat = []
sa = []
sm = []
sf = []
sp = []
si = []

# Setup Simulation Loops
for i in xrange(2):
    for j in xrange(3):
        for k in xrange(9):
            # Set Launch/Recovery System
            if i == 0:
                system = Crane1
            else:
                system = Crane2
            # Set the vehicle
            if j == 0:
                vehicle = veh1
            elif j == 1:
                vehicle = veh2
            else:
                vehicle = veh3
            # Set the environment
            env = Environment('SS',k,k)

            # Setup the simulation
            sim = Simulation(ship,vehicle,system,env)

            # Run the Simulation
            sim.run()

            # Save the output
            sat.append(sim.get_satisfaction())
            sa.append(sim.sat_a)
            sm.append(sim.sat_m)
            sf.append(sim.sat_f)
            sp.append(sim.sat_p)
            si.append(sim.sat_i)

# Write Output to a File
with open('case_study.csv','wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(sat)
    wr.writerow(sa)
    wr.writerow(sm)
    wr.writerow(sf)
    wr.writerow(sp)
    wr.writerow(si)

# Create Plots
ss_vec = [1,2,3,4,5,6,7,8,9]

# Figure 1: System 1
plt.figure()
plt.plot(ss_vec,sat[0:9], 'o-C0', label = 'Small UUV')
plt.plot(ss_vec,sat[9:18], '^-C1', label = 'Medium RHIB')
plt.plot(ss_vec,sat[18:27], 's-C2', label = 'Heavy RHIB')
plt.legend()
plt.xlabel('Sea State Rating')
plt.ylabel(r'P($\theta$)')
plt.ylim(0, 1)
plt.grid()
plt.savefig('output/case_study_1.png',format='png')

# Figure 2: System 2
plt.figure()
plt.plot(ss_vec,sat[27:36], 'o-C0', label = 'Small UUV')
plt.plot(ss_vec,sat[36:45], '^-C1', label = 'Medium RHIB')
plt.plot(ss_vec,sat[45:54], 's-C2', label = 'Heavy RHIB')
plt.legend()
plt.xlabel('Sea State Rating')
plt.ylabel(r'P($\theta$)')
plt.ylim(0, 1)
plt.grid()
plt.savefig('output/case_study_2.png',format='png')

# Figure 3: System 1, Medium RHIB
plt.figure()
plt.plot(ss_vec,sat[9:18], 'o-C1', label = r'$\theta$')
plt.plot(ss_vec,sa[9:18], '^-C2', label = r'$\theta_a$')
plt.plot(ss_vec,sm[9:18], 'v-C3', label = r'$\theta_m$')
plt.plot(ss_vec,sp[9:18], 'x-C4', label = r'$\theta_p$')
plt.plot(ss_vec,si[9:18], '*-C5', label = r'$\theta_i$')
plt.plot(ss_vec,sf[9:18], 's-C6', label = r'$\theta_f$')

plt.legend()
plt.xlabel('Sea State Rating')
plt.ylabel(r'P($\theta$)')
plt.ylim(0, 1)
plt.grid()
plt.savefig('output/case_study_3.png',format='png')

# Figure 4: Compare System 1 and System 2 for Medium RHIB
plt.figure()
plt.plot(ss_vec,sat[9:18], 'o-C1', label = 'System 1')
plt.plot(ss_vec,sat[36:45], '^-C2', label = 'System 2')

plt.legend()
plt.xlabel('Sea State Rating')
plt.ylabel(r'P($\theta$)')
plt.ylim(0, 1)
plt.grid()
plt.savefig('output/case_study_4.png',format='png')

# Figure 5: System 1 - System 2 for Medium RHIB
difference = []
difference.append(sat[9]-sat[36])
difference.append(sat[10]-sat[37])
difference.append(sat[11]-sat[38])
difference.append(sat[12]-sat[39])
difference.append(sat[13]-sat[40])
difference.append(sat[14]-sat[41])
difference.append(sat[15]-sat[42])
difference.append(sat[16]-sat[43])
difference.append(sat[17]-sat[44])

plt.figure()
plt.plot(ss_vec,difference, 'o-C1', label = 'Difference')

plt.legend()
plt.xlabel('Sea State Rating')
plt.ylabel(r'P($\theta$)')
plt.ylim(0, 1)
plt.grid()
plt.savefig('output/case_study_5.png',format='png')

# Figure 6: S1&2 MD RHIB and Difference
plt.figure()
plt.plot(ss_vec,sat[9:18], 'o-C1', label = 'System 1')
plt.plot(ss_vec,sat[36:45], '^-C2', label = 'System 2')
plt.plot(ss_vec,difference, 's-C3', label = 'Difference')

plt.legend()
plt.xlabel('Sea State Rating')
plt.ylabel(r'P($\theta$)')
plt.ylim(0, 1)
plt.grid()
plt.savefig('output/case_study_6.png',format='png')
