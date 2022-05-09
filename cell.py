import networkx as nx
from random import randint, random
from math import tanh
from funcs import *

class Cell:
	def __init__(self, genome, neurons):
		self.brain = nx.DiGraph()
		self.neurons = neurons
		self.genome = genome
		self.decode_genome(genome, neurons)
		self.pos_x = 0
		self.pos_y = 0

	def parse_genome(self):
		for gene in self.genome:
			if (gene[0:2], gene[2:4]) not in self.brain.edges:
				self.brain.add_edge(
					gene[0:2],
					gene[2:4],
					weight = normalise(int(gene[4:6], 16)) * 4.0) 
		for neuron in self.brain.nodes:
			self.brain.nodes[neuron]['output'] = 0.0

	def decode_genome(self, genome, neurons):
		for gene in genome:
			for i in range(0, len(gene), 2):
				if i in [0,2]:					
					neuron = ''.join(
						[neuron for neuron in self.neurons \
						if (self.neurons[neuron]['type'] == \
						['sensory','action','internal'][int(gene[i])]) \
						and (self.neurons[neuron]['index'] == \
						int(gene[i+1]))])
					if i == 0:
						u_neuron = neuron
					elif i == 2:
						v_neuron = neuron
				elif i == 4:
					weight = normalise(int(gene[4:6], 16)) * 4.0
			if (u_neuron, v_neuron) not in self.brain.edges:
				self.brain.add_edge(u_neuron, v_neuron, weight=weight)
		for node in self.brain.nodes:
			self.brain.nodes[node]['output'] = 0.5		

	def check_sensory(self):
		for neuron in self.brain.nodes: 
			if self.neurons[neuron]['type'] == 'sensory':
				"""if randint(0, 1):
					self.brain.nodes[str(neuron)]['output'] = 1.0
				else: 
					self.brain.nodes[str(neuron)]['output'] = 0.0"""
				self.brain.nodes[str(neuron)]['output'] = random()

	def sum_neuron_inputs(self, neuron):
		inputs_sum = 0
		for u_neuron, v_neuron, data in self.brain.edges(data=True): 
			if v_neuron == neuron:
				inputs_sum += \
				data['weight'] * self.brain.nodes[neuron]['output']
		self.brain.nodes[str(neuron)]['output'] = ((tanh(inputs_sum)+1)/2)
		#self.brain.nodes[str(neuron)]['output'] = ((max(0, inputs_sum)+1)/2)

	def step(self):
		self.check_sensory()
		for neuron_type in ['internal', 'action']:
			for neuron in self.brain.nodes:
				if self.neurons[neuron]['type'] == neuron_type:
					self.sum_neuron_inputs(neuron)
		self.an_move_x()
		self.an_move_y()
	
	def an_move_x(self):
		if self.brain.nodes['aMvX']['output'] >= 0.1:
			self.pos_x += 1
		elif self.brain.nodes['aMvX']['output'] <= (-0.1):
			self.pos_x -= 1

	def an_move_y(self):
		if self.brain.nodes['aMvY']['output'] >= 0.1:
			self.pos_y += 1
		elif self.brain.nodes['aMvY']['output'] <= (-0.1):
			self.pos_y -= 1
