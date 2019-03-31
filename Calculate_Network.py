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

# Define Classes

class Host_Ship(object):
	"""
	Host Ship class, which encapsulates the properties of  the host ship
	"""

	def __init__(self,name,arr_flex,size_crew,fbd_min):

		self.name = name # what ship
		self.arr_flex = arr_flex # rate 1-9 (9 is best)
		self.size_crew = size_crew # actual number
		self.fbd_min = fbd_min # in meters

	def get_name(self):
		return self.name

	def get_arr_flex(self):
		return self.arr_flex

	def get_size_crew(self):
		return self.size_crew

	def get_fbd_min(self):
		return self.fbd_min

class Vehicle(object):
	"""
	Vehicle class, which encapsulates the properties of the L/R Vehicle
	"""

	def __init__(self,name,volume,weight,variability,flexibility,complexity):

		self.name = name
		self.vol = volume # cu m
		self.weight = weight # mt
		self.var = variability # 1 to 9
		self.flex = flexibility # 1 to 9
		self.cmplx = complexity # 1 to 9

	def get_name(self):
		return self.name

	def get_volume(self):
		return self.vol

	def get_weight(self):
		return self.weight

	def get_var(self):
		return self.var

	def get_flex(self):
		return self.flex

	def get_cmplx(self):
		return self.cmplx

class LR_system(object):
	"""
	Launch & Recovery Sysem class, encapsulates the properties of the L/R System
	"""

	def __init__(self,name,req,fbd_flex,rel_height,cap):

		self.name = name
		self.req = req # system requirements level, 1-9
		self.fbd_flex = fbd_flex # 1-9
		self.rel_height = rel_height #1-9
		self.cap = cap # mt

	def get_name(self):
		return self.name

	def get_sys_req(self):
		return self.req

	def get_fbd_flex(self):
		return self.fbd_flex

	def get_rel_height(self):
		return self.rel_height

	def get_cap(self):
		return self.cap

class Environment(object):
	"""
	Environment class, which encapsulates the properties of the Environment
	"""

	def __init__(self,name,ss,wind):

		self.name = name
		self.ss = ss # 1-9
		self.wind = wind #1-9

	def get_name(self):
		return self.name

	def get_ss(self):
		return self.ss

	def get_wind(self):
		return self.wind

# Define Probability Tables
def prob_satisfied_metric(metric):
	lookup = round(metric)

	if lookup <= 1:
		return 0.99
	elif lookup == 2:
		return 0.98
	elif lookup == 3:
		return 0.95
	elif lookup == 4:
		return 0.8
	elif lookup == 5:
		return 0.5
	elif lookup == 6:
		return 0.2
	elif lookup == 7:
		return 0.1
	elif lookup == 8:
		return 0.05
	else:
		return 0.01

def prob_impacted_metric(metric):
	return 1 - prob_satisfied_metric(metric)

def prob_arrangement_impact(volume):
	if volume <= 0.1:
		return 0.01
	elif volume <= 1:
		return 0.05
	elif volume <= 5:
		return 0.15
	elif volume <= 10:
		return 0.25
	elif volume <= 20:
		return 0.45
	elif volume <= 30:
		return 0.60
	elif volume <= 40:
		return 0.7
	elif volume <= 50:
		return 0.78
	elif volume <= 75:
		return 0.9
	elif volume <= 100:
		return 0.95
	else:
		return 0.99

def prob_manning_impact(weight):
	if weight <= 1:
		return 0.01
	elif weight <= 5:
		return 0.02
	elif weight <= 10:
		return 0.05
	elif weight <= 20:
		return 0.1
	elif weight <= 30:
		return 0.2
	elif weight <= 40:
		return 0.3
	elif weight <= 50:
		return 0.4
	elif weight <= 100:
		return 0.6
	else:
		return 0.7

def prob_enough_crew(crew_size):
	if crew_size <= 5:
		return 0.01
	elif crew_size <= 10:
		return 0.08
	elif crew_size <= 15:
		return 0.15
	elif crew_size <= 20:
		return 0.2
	elif crew_size <= 30:
		return 0.3
	elif crew_size <= 40:
		return 0.4
	elif crew_size <= 50:
		return 0.5
	elif crew_size <= 60:
		return 0.6
	elif crew_size <= 80:
		return 0.72
	elif crew_size <= 100:
		return 0.8
	elif crew_size <= 150:
		return 0.9
	elif crew_size <= 200:
		return 0.95
	else:
		return 0.99

def prob_enough_fbd(fbd_min):
	if fbd_min <= 0.5:
		return 0.99
	elif fbd_min <= 1:
		return 0.95
	elif fbd_min <= 2:
		return 0.85
	elif fbd_min <= 3:
		return 0.75
	elif fbd_min <= 4:
		return 0.65
	elif fbd_min <= 5:
		return 0.55
	elif fbd_min <= 6:
		return 0.45
	elif fbd_min <= 7:
		return 0.35
	elif fbd_min <= 8:
		return 0.25
	elif fbd_min <= 9:
		return 0.15
	else:
		return 0.05

# Setup Calculation Function
class Simulation(object):
	"""
	Simulates a loop through the network
	"""

	def __init__(self,ship,vehicle,system,environment):
		self.ship = ship
		self.vehicle = vehicle
		self.system = system
		self.environment = environment

		self.sat_a = 0
		self.sat_f = 0
		self.sat_p = 0
		self.sat_i = 0
		self.sat_m = 0
		self.sat = 0

	def run(self):
		# Calculate Available Manning - P(Enough Crew)
		# Needs Crew Size, Sea State, and Wind
		man_avail = prob_enough_crew(self.ship.get_size_crew()) * prob_satisfied_metric(self.environment.wind) * prob_satisfied_metric(self.environment.ss)

		# Calculate Arrangement Impact - P(Satisfied)
		# Needs Vehicle Volume, System Requirements
		imp = 1 - prob_arrangement_impact(self.vehicle.get_volume()) * prob_impacted_metric(self.system.get_sys_req())


		# Calculate Required Manning - P(Satisfied)
		# Needs vehicle weight, system, sea state, and wind
		# Reuse env_metric
		man_req = prob_satisfied_metric(self.environment.wind) * prob_satisfied_metric(self.environment.ss) * (1-prob_manning_impact(self.vehicle.get_weight())) * prob_satisfied_metric(self.system.get_sys_req())

		# Calculate L/R System Simplicity - P(Satisfied)
		# Needs Relative height, sea state, wind
		simplicity = prob_satisfied_metric(self.environment.wind) * prob_satisfied_metric(self.environment.ss) * prob_satisfied_metric(self.system.get_rel_height())

		# Calculate Actual Capacity - Capcity in mt
		# Needs rated capacity, and environmental conditions
		rated_cap = self.system.get_cap()
		detriment = prob_impacted_metric(self.environment.wind) * prob_impacted_metric(self.environment.ss) * rated_cap
		actual_cap = rated_cap - 0.5*detriment

		# Calculate Freeboard Available - P(Satisfied)
		# Needs Sea State
		fbd_avail = prob_satisfied_metric(self.environment.ss)

		# Calculate Arrangement Satisfaction
		# From Arrangement flexibility, impact, and system req
		flex = prob_satisfied_metric(self.ship.get_arr_flex())
		sys_sat = prob_satisfied_metric(self.system.get_sys_req())
		self.sat_a = imp * flex * sys_sat
		#print("Arrangement Satisfaction %f") % sat_a

		# Calculate Manning Satisfaction
		# Need Available Manning and Required Manning
		self.sat_m = man_req * man_avail
		#print("Manning Satisfaction %f") % sat_m

		# Calculate Freeboard Satisfaction
		# Need Freeboard min, flexibility, and available
		self.sat_f = fbd_avail * prob_satisfied_metric(self.system.get_fbd_flex()) * prob_enough_fbd(self.ship.get_fbd_min())
		#print("Freeboard Satisfaction %f") % sat_f

		# Calculate Performance Satisfaction
		# Ned Simplicity, Actual Capacity, Complexity, Weight
		weight = self.vehicle.get_weight()
		if weight > actual_cap:
			self.sat_p = 0.01
			#print("Weight greater than capacity")
		else:
			self.sat_p = (1-weight/actual_cap) + 0.25
			if self.sat_p > 1: self.sat_p = 1
			# print(self.sat_p)
			self.sat_p = self.sat_p * prob_satisfied_metric(self.vehicle.get_cmplx()) * simplicity
		#print("Performance Satisfaction %f") % sat_p

		# Calcualte Interoperability Satisfaction
		# Need Vehicle Variability and L/R Flexibility
		self.sat_i = prob_satisfied_metric((self.vehicle.get_var() + self.vehicle.get_flex())/2)
		#print("Vehicle Interoperability Satisfaction %f") % sat_i

		# Calculate Overall Satisfaction
		self.sat = self.sat_a * self.sat_m * self.sat_f * self.sat_p * self.sat_i
		# For Geometric Mean:
		self.sat = self.sat ** (1/5)
		#print("Overall Probability of Satisfaction %f") % sat

	def get_satisfaction(self):
		return self.sat

	def get_sub_vector(self):
		sub_vector = []
		sub_vector.append(self.sat_f)
		sub_vector.append(self.sat_a)
		sub_vector.append(self.sat_m)
		sub_vector.append(self.sat_p)
		sub_vector.append(self.sat_i)
		return sub_vector

# Function call that does the same thing as the class
def determine_outcome(ship, vehicle, system, environment):

	# Calculate Available Manning - P(Enough Crew)
	# Needs Crew Size, Sea State, and Wind
	env_metric = (environment.get_ss() + environment.get_wind())/2
	man_avail = prob_enough_crew(ship.get_size_crew()) * prob_satisfied_metric(env_metric)

	# Calculate Arrangement Impact - P(Satisfied)
	# Needs Vehicle Volume, System Requirements
	imp = 1 - prob_arrangement_impact(vehicle.get_volume()) * prob_impacted_metric(system.get_sys_req())

	# Calculate Required Manning - P(Satisfied)
	# Needs vehicle weight, system, sea state, and wind
	# Reuse env_metric
	man_req = prob_satisfied_metric(env_metric) * (1-prob_manning_impact(vehicle.get_weight())) * prob_satisfied_metric(system.get_sys_req())

	# Calculate L/R System Simplicity - P(Satisfied)
	# Needs Relative height, sea state, wind
	simplicity = prob_satisfied_metric(env_metric) * prob_satisfied_metric(system.get_rel_height())

	# Calculate Actual Capacity - Capcity in mt
	# Needs rated capacity, and environmental conditions
	rated_cap = system.get_cap()
	detriment = prob_impacted_metric(env_metric) * rated_cap
	actual_cap = rated_cap - 0.5*detriment

	# Calculate Freeboard Available - P(Satisfied)
	# Needs Sea State
	fbd_avail = prob_satisfied_metric(environment.get_ss())

	# Calculate Arrangement Satisfaction
	# From Arrangement flexibility, impact, and system req
	flex = prob_satisfied_metric(ship.get_arr_flex())
	sys_sat = prob_satisfied_metric(system.get_sys_req())
	sat_a = imp * flex * sys_sat
	print("Arrangement Satisfaction %f") % sat_a

	# Calculate Manning Satisfaction
	# Need Available Manning and Required Manning
	sat_m = man_req * man_avail
	print("Manning Satisfaction %f") % sat_m

	# Calculate Freeboard Satisfaction
	# Need Freeboard min, flexibility, and available
	sat_f = fbd_avail * prob_satisfied_metric(system.get_fbd_flex()) * prob_enough_fbd(ship.get_fbd_min())
	print("Freeboard Satisfaction %f") % sat_f

	# Calculate Performance Satisfaction
	# Ned Simplicity, Actual Capacity, Complexity, Weight
	weight = vehicle.get_weight()
	if weight > actual_cap:
		sat_p = 0.01
		print("Weight greater than capacity")
	else:
		sat_p = (1-weight/actual_cap) + 0.25
		if sat_p > 1: sat_p = 1
		sat_p = sat_p * prob_satisfied_metric(vehicle.get_cmplx()) * simplicity
	print("Performance Satisfaction %f") % sat_p

	# Calcualte Interoperability Satisfaction
	# Need Vehicle Variability and L/R Flexibility
	sat_i = prob_satisfied_metric((vehicle.get_var() + vehicle.get_flex())/2)
	print("Vehicle Interoperability Satisfaction %f") % sat_i

	# Calculate Overall Satisfaction
	sat = sat_a * sat_m * sat_f * sat_p * sat_i
	# For Geometric Mean:
	sat = sat ** (1/5)
	print("Overall Probability of Satisfaction %f") % sat
	return sat
