import random
import itertools
import networkx as nx 
import bitarray
import bitarray.util
import calc
import genetics


class Animal:
	
	def __init__(self, args, genome, neurons, x=0, y=0):
		self.args = args
		self.type = 'animal'
		self.brain = nx.DiGraph()
		self.neurons = neurons
		self.genome = genome
		self.colour = []
		self.decode_genome()
		self.x = x
		self.y = y
		self.wild_range = []
		self.age = 0
		self.energy = 0
		self.pain = 0
		self.neuron_functions = {
			'sDtA' : self.detect_animal,
			'sDtP' : self.detect_plant,
			'sDpX' : self.detect_pos_x,
			'sDnX' : self.detect_neg_x,
			'sDpY' : self.detect_pos_y,
			'sDnY' : self.detect_neg_y,
			'sDpn' : self.detect_pain}

	def get_wild_range(self, wild, wild_range):
		for x, y in itertools.product([-1, 1], [-1, 1]):
			if (self.x + x, self.y + y) in wild.valid_wild:
				wild_range.append((self.x + x, self.y + y))
		return wild_range

	def decode_genome(self, mutation_chance=0.01):
		colours = []
		for gene in self.genome:
			if random.random() <= mutation_chance:
				gene = self.mutate(gene)
			colours.append(self.get_colour(gene))
			self.decode_gene(gene)
		self.colour = self.average_colour(colours, self.colour)

	def mutate(self, gene):
		gene[random.sample([i for i in range(24)], 1)[0]] \
		= random.getrandbits(1)
		return gene

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
	
	def decode_neuron(self, 
		neuron_type, neuron_toggle, neuron_id, neuron_id_range=64):
		neurons = [neuron for neuron in self.neurons
			if self.neurons[neuron]["type"]
			==[neuron_type, "internal"][neuron_toggle]]
		
		return f'''{[
			neuron for neuron in neurons
			if self.neurons[neuron]["id"]
			== [(neuron_id_range / len(neurons)) * i 
			for i, _ in enumerate(neurons)].index(
				min([(neuron_id_range / len(neurons)) * i 
				for i, _ in enumerate(neurons)],
					key=lambda x:abs(x - neuron_id)))][0]}'''

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
	
	def action(self, term, wild, soil, turn_stack):
		
		self.wild_range = self.get_wild_range(wild, self.wild_range)
		if self.pain > 0:
			self.pain -= 1

		for neuron in self.brain.nodes: 
			if self.neurons[neuron]['type'] == 'sensory':
				self.neuron_functions[neuron](wild, soil)
		
		for neuron in self.brain.nodes:
			if self.neurons[neuron]['type'] in ['internal', 'action']:
				self.sum_neuron_inputs(neuron)
		
		self.process_movement(wild)
		
		if soil.soil[self.x][self.y]['plant']:
			self.energy += soil.soil[self.x][self.y]['plant_energy']
			soil.soil[self.x][self.y]['plant'] = None
			soil.soil[self.x][self.y]['plant_energy'] = 0
			soil.soil[self.x][self.y]['dung'] = True

		if self.energy >= 30:	
			self.reproduce(term, wild, soil, turn_stack)
		
		self.age += 1
		return self.death()

	def detect_animal(self, wild, soil):
		nearby_animals = self.detect(wild, soil, 'animal')
		self.brain.nodes['sDtA']['output'] = (1 / 8) * nearby_animals

	def detect_plant(self, wild, soil):
		nearby_plants = self.detect(wild, soil, 'plant')
		self.brain.nodes['sDtP']['output'] = (1 / 8) * nearby_plants

	def detect(self, wild, soil, target):
		count = 0
		open_space = []
		for x, y in self.wild_range:
			if target == 'animal':	
				if wild.wild[x][y]['occupant']:
					count += 1
			elif target == 'plant':
				if soil.soil[x][y]['plant']:
					count += 1
			elif target == 'space':
				if wild.wild[x][y]['occupant'] == None:
					open_space.append((x, y))
		if target != 'space':
			return count
		elif target == 'space':
			return open_space

	def sum_neuron_inputs(self, neuron):
		self.brain.nodes[neuron]['output'] = calc.activation(
			sum([
				(data['weight'] * self.brain.nodes[u_neuron]['output']) \
				for u_neuron, v_neuron, data in self.brain.edges(data=True) \
				if v_neuron == neuron]), 
				'tanh')

	def process_movement(self, wild):	
		neuron_data = [['aMvX', 0, self.x], ['aMvY', 0, self.y]]
		for data in neuron_data:
			if data[0] in self.brain.nodes:
				if self.brain.nodes[data[0]]['output'] >= 0.9:
					if (data[2] + 1) <= self.args.environment:
						data[1] = 1
				elif self.brain.nodes[data[0]]['output'] <= (-0.9):
					if (data[2] - 1) >= 1:
						data[1] = -1

		if wild.wild\
		[self.x + neuron_data[0][1]]\
		[self.y + neuron_data[1][1]]\
		['occupant'] == None:
			self.x += neuron_data[0][1]
			self.y += neuron_data[1][1]
		if wild.wild[self.x][self.y]['effect'] == 'pain':
			self.pain += 1

	def reproduce(self, term, wild, soil, turn_stack):	
		open_space = self.detect(wild, soil, 'space')
		if len(open_space) != 0:		
			x, y = random.sample(open_space, 1)[0]
			wild.animals.append(Animal(
				self.args, self.genome, self.neurons, x, y))
			turn_stack.append(wild.animals[-1])
			print(
				term.move_xy(wild.animals[-1].x, wild.animals[-1].y) + 
				term.color_rgb(
					wild.animals[-1].colour[0], 
					wild.animals[-1].colour[1], 
					wild.animals[-1].colour[2]) 
					+ '@')
			wild.wild[x][y]['occupant'] = wild.animals[-1]
			self.energy -= 20

	def death(self):
		if self.age == 50:
			return True
		if self.pain == 5:
			return True

	def detect_edge(self, polarity, axis):
		if polarity == 'positive':
			return (1 / self.args.environment) * axis
		elif polarity == 'negative':
			return (1 / self.args.environment) * (self.args.environment - axis)

	def detect_pos_x(self, wild, soil):
		self.brain.nodes['sDpX']['output'] = self.detect_edge(
			'positive', self.x)

	def detect_neg_x(self, wild, soil):
		self.brain.nodes['sDnX']['output'] = self.detect_edge(
			'negative', self.x)

	def detect_pos_y(self, wild, soil):
		self.brain.nodes['sDpY']['output'] = self.detect_edge(
			'positive', self.y)

	def detect_neg_y(self, wild, soil):
		self.brain.nodes['sDnY']['output'] = self.detect_edge(
			'negative', self.y)

	def detect_pain(self):
		if self.pain > 0:
			return 1.0
		else:
			return 0.0




