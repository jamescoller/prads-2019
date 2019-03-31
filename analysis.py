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
shipA = Host_Ship('A',3,200,1)
# Vehicle: (self,name,volume,weight,variability,flexibility,complexity)
vehA = Vehicle('A',15,20,3,3,2)
# System: (self,name,req,fbd_flex,rel_height,cap)
crane = LR_system('Crane',4,2,2,40)
# Environment: (self,name,ss,wind)
ss2 = Environment('SS2',2,2)

# Baseline
baseline = Simulation(shipA, vehA, crane, ss2)
baseline.run()
print(baseline.sat)
print(baseline.get_sub_vector())

# Plot the Baseline
total_vector = [baseline.sat]
total_vector += baseline.get_sub_vector()

# Show the figure, but do not block
plt.show(block=False)
plt.figure()
fig, ax = plt.subplots()
ind = np.arange(1,7)
s1, s2, s3, s4, s5, s6 = plt.bar(ind, total_vector)

s1.set_facecolor('C0')
s2.set_facecolor('C1')
s3.set_facecolor('C2')
s4.set_facecolor('C3')
s5.set_facecolor('C4')
s6.set_facecolor('C9')


plt.xticks(ind,('Overall\nSatisfaction','Freeboard','Arrangement\nFlexibility','Manning','Performance','Interoperability'))
plt.xticks(rotation=45)
ax.set_xlabel('Metric')
#ax.set_xticks(ind)
#ax.set_xticklabels(['Overall','Freeboard','Arrangement Flexibility','Manning','Performance','Interoperability'])
ax.set_ylabel('P(Satisfied)')
plt.suptitle('Baseline Performance')
plt.gcf().subplots_adjust(bottom=0.25)
plt.ylim(0, 1)
plt.savefig("output/baseline.png")


# Setup Sea State Parameter Sweep
sim_history = []
sat_history = []
a_history = []
m_history = []
f_history = []
p_history = []
i_history = []

values = np.arange(1,10)
#values = [1,5,10,20,30,40,50,100,200] # Weight
#values = [0.1,1,5,10,20,30,40,50,75,100,150] # Volume
#values = [5,10,15,20,30,40,50,60,80,100,150,200,400] # Crew Size

what_var = 13

for i in range(len(values)):
    # What are we changing?
    ss = Environment('SS2',2,values[i])
    # Use the rest of the inputs as the same from before
    sim = Simulation(shipA, vehA, crane, ss)
	# Run the simulation
    sim.run()
	# Get the Satisfaction
    sim_history.append(sim)
    sat_history.append(sim.get_satisfaction())

    a_history.append(sim.sat_a)
    m_history.append(sim.sat_m)
    f_history.append(sim.sat_f)
    p_history.append(sim.sat_p)
    i_history.append(sim.sat_i)


# Plotting and Analysis
plt.figure()
sat_probs = [0.99, 0.98, 0.95, 0.8, 0.5, 0.2, 0.1, 0.05, 0.01]
simple_vec = [1,2,3,4,5,6,7,8,9]
labels = ['Freeboard','Arrangement Flexibility','Manning','Performance','Interoperability']

#plt.plot(simple_vec,sat_history, 'o-',label = 'Overall Satisfaction')
#plt.plot(simple_vec,sat_probs, 'D--',label= 'Sea State P(Impact)')
#plt.ylabel('P(Satisfaction)')
#plt.xlabel('Sea State Rating')
#plt.legend()
#plt.grid()

#plt.gcf().subplots_adjust(bottom=0.10)
#plt.savefig('output/ss_plot.png',format='png')

plt.figure()
#plt.plot(simple_vec,sat_history, 'o-C0', label = 'Overall Satisfaction')
#plt.plot(simple_vec,f_history,'^-C1',label = labels[0])
#plt.plot(simple_vec,a_history,'v-C2',label = labels[1])
#plt.plot(simple_vec,m_history,'x-C3',label = labels[2])
#plt.plot(simple_vec,p_history,'*-C4',label = labels[3])
#plt.plot(simple_vec,i_history,'s-C9',label = labels[4])
plt.legend()
plt.grid()
plt.ylabel('P(Satisfaction)')
plt.xlabel('Sea State Rating')
#plt.savefig('output/ss_plot_2.png',format='png')

# plt.show()

headers = ['Value','Overall','sf','sa','sm','sp','si']

# Automate the Shitty Analysis
file_names = [
'history/arr_flex.csv',
'history/crew_size.csv',
'history/fbd_min.csv',
'history/volume.csv',
'history/weight.csv',
'history/variability.csv',
'history/flexibility.csv',
'history/complexity.csv',
'history/sys_req.csv',
'history/fbd_flex.csv',
'history/rel_height.csv',
'history/capacity.csv',
'history/sea_state.csv',
'history/wind.csv',
]

# Write Output to a File
with open(file_names[what_var],'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(values)
    wr.writerow(sat_history)
    wr.writerow(f_history)
    wr.writerow(a_history)
    wr.writerow(m_history)
    wr.writerow(p_history)
    wr.writerow(i_history)
