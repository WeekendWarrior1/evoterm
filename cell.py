import networkx as nx
from random import randint, random
from funcs import *

class Cell:
	def __init__(self, genome, neurons):
		self.brain = nx.DiGraph()
		self.neurons = neurons
		self.genome = genome
		self.decode_genome(genome, neurons)
		self.pos_x = 0
		self.pos_y = 0

	def check_neuron_type(self, gene, i):
		return f'''{[
			neuron for neuron in self.neurons 
			if (self.neurons[neuron]["type"] 
			== ["sensory","action","internal"][int(gene[i])]) 
			and (self.neurons[neuron]["id"] 
			== int(gene[i+1]))][0]}'''

	def decode_genome(self, genome, neurons):
		for gene in genome:
			for i in range(0, len(gene), 2):
				if i != 4:
					if not i:
						u_neuron = self.check_neuron_type(gene, i)
					else:
						v_neuron = self.check_neuron_type(gene, i)
			if (u_neuron, v_neuron) not in self.brain.edges:
				self.brain.add_edge(
					u_neuron, 
					v_neuron, 
					weight = normalise(int(gene[4:6], 16)) * 4.0)
		for node in self.brain.nodes:
			self.brain.nodes[node]['output'] = 0.5		

	def check_sensory(self):
		for neuron in self.brain.nodes: 
			if self.neurons[neuron]['type'] == 'sensory':
				self.brain.nodes[neuron]['output'] = random()

	def sum_neuron_inputs(self, neuron):
		self.brain.nodes[neuron]['output'] = activation(
			sum([
				(data['weight'] * self.brain.nodes[neuron]['output']) \
				for u_neuron, v_neuron, data in self.brain.edges(data=True) \
				if v_neuron == neuron]), 
			'tanh')

	def step(self):
		self.check_sensory()
		for neuron in self.brain.nodes:
			if self.neurons[neuron]['type'] in ['internal', 'action']:
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
