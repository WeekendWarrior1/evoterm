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
		self.colour = []
		self.decode_genome()
		self.pos_x = 0
		self.pos_y = 0

	def decode_genome(self, mutation_chance=0.01):
		colours = []
		for gene in self.genome:
			if random.random() <= mutation_chance:
				gene = self.mutate(gene)
			colours.append(self.get_colour(gene))
			self.decode_gene(gene)
		self.colour = self.average_colour(colours, self.colour)

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
	
	def decode_neuron(self, neuron_type, neuron_toggle, neuron_id, neuron_id_range=64):
		neurons = [neuron for neuron in self.neurons
			if self.neurons[neuron]["type"]
			==[neuron_type, "internal"][neuron_toggle]]
		
		return f'''{[
			neuron for neuron in neurons
			if self.neurons[neuron]["id"]
			== [(neuron_id_range / len(neurons)) * i for i in range(len(neurons))].index(
				min(
					[(neuron_id_range / len(neurons)) * i for i in range(len(neurons))],
					key=lambda x:abs(x - neuron_id)))][0]}'''

	def mutate(self, gene):
		gene[random.sample([i for i in range(24)], 1)[0]] = random.getrandbits(1)
		return gene

	def get_colour(self, gene):
		r = bitarray.util.ba2int(gene[0:8])
		g = bitarray.util.ba2int(gene[8:16])
		b = bitarray.util.ba2int(gene[16:24])
		return [r, g, b]

	def average_colour(self, colours_in, colours_out):
		for i in range(3):
			tmp = []
			for colour in colours_in:
				tmp.append(colour[i])
			colours_out.append(sum(tmp) // len(tmp))

		return colours_out
	
	def fire_neurons(self, env_size, occupied_coordinates):
		self.check_sensory()
		
		for neuron in self.brain.nodes:
			if self.neurons[neuron]['type'] in ['internal', 'action']:
				self.sum_neuron_inputs(neuron)
		
		self.process_movement(occupied_coordinates, env_size)

	def check_sensory(self):
		for neuron in self.brain.nodes: 
			if self.neurons[neuron]['type'] == 'sensory':
				self.brain.nodes[neuron]['output'] = random.random()

	def sum_neuron_inputs(self, neuron):
		self.brain.nodes[neuron]['output'] = calc.activation(
			sum([
				(data['weight'] * self.brain.nodes[u_neuron]['output']) \
				for u_neuron, v_neuron, data in self.brain.edges(data=True) \
				if v_neuron == neuron]), 
			'tanh')

	def process_movement(self, occupied_coordinates, env_size):
		if 'aMvX' in self.brain.nodes:
			x = self.brain.nodes['aMvX']['output']	
			if x >= 0.1:
				if (self.pos_x + 1) <= env_size:
					x = 1
			elif x <= (-0.1):
				if (self.pos_x - 1) >= 1:
					x = (-1)
			else:
				x = 0
		else: 
			x = 0

		if 'aMvY' in self.brain.nodes:
			y = self.brain.nodes['aMvY']['output']
			if y >= 0.1:
				if (self.pos_y + 1) <= env_size:
					y = 1
			elif y <= (-0.1):
				if (self.pos_y - 1) >= 1:
					y = (-1)
			else:
				y = 0
		else:
			y = 0

		for i in [(-1), 0, 1]:
			if (self.pos_x + x, self.pos_y + i) not in occupied_coordinates:
				if y == i:
					self.pos_x += int(x)
					self.pos_y += int(i)

