import random
import networkx as nx 
import bitarray
import bitarray.util
import calc


class Cell:
	
	def __init__(self, genome, neurons):
		self.brain = nx.DiGraph()
		self.neurons = neurons
		self.genome = genome
		self.decode_genome()
		self.pos_x = 0
		self.pos_y = 0

	def decode_genome(self):
		for gene in self.genome:
			self.decode_gene(gene)

	def decode_gene(self, gene):
		u_neuron = \
			self.decode_neuron(
				"sensory", gene[-1], bitarray.util.ba2int(gene[-6:-1]))
		v_neuron = \
			self.decode_neuron(
				"action", gene[-7], bitarray.util.ba2int(gene[-12:-7]))
		
		if (u_neuron, v_neuron) not in self.brain.edges:
			self.brain.add_edge(
				u_neuron,
				v_neuron,
				weight = calc.normalise(
					polarity = gene[-13], 
					x = bitarray.util.ba2int(gene[-24:-13])) * 4)
		
		for node in self.brain.nodes:
			self.brain.nodes[node]['output'] = 0.5		
	
	def decode_neuron(self, neuron_type, neuron_toggle, neuron_id):
		return f'''{[
			neuron for neuron in self.neurons 
			if (self.neurons[neuron]["type"] 
			== [neuron_type, "internal"][neuron_toggle]) 
			and (self.neurons[neuron]["id"] 
			== neuron_id)][0]}'''
	
	def step(self):
		self.check_sensory()
		
		for neuron in self.brain.nodes:
			if self.neurons[neuron]['type'] in ['internal', 'action']:
				self.sum_neuron_inputs(neuron)
		
		if 'aMvX' in self.brain.nodes:
			self.action_move_x()
		if 'aMvY' in self.brain.nodes:
			self.action_move_y()

	def check_sensory(self):
		for neuron in self.brain.nodes: 
			if self.neurons[neuron]['type'] == 'sensory':
				self.brain.nodes[neuron]['output'] = random.random()

	def sum_neuron_inputs(self, neuron):
		self.brain.nodes[neuron]['output'] = calc.activation(
			sum([
				(data['weight'] * self.brain.nodes[neuron]['output']) \
				for u_neuron, v_neuron, data in self.brain.edges(data=True) \
				if v_neuron == neuron]), 
			'tanh')

	def action_move_x(self):
		if self.brain.nodes['aMvX']['output'] >= 0.1:
			self.pos_x += 1
		elif self.brain.nodes['aMvX']['output'] <= (-0.1):
			self.pos_x -= 1

	def action_move_y(self):
		if self.brain.nodes['aMvY']['output'] >= 0.1:
			self.pos_y += 1
		elif self.brain.nodes['aMvY']['output'] <= (-0.1):
			self.pos_y -= 1

