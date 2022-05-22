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

	def action(self, term, wild, soil):
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
		
		if random.randint(0, 10) == 0:
			soil.soil[self.x][self.y]['dung'] = True

		if soil.soil[self.x][self.y]['plant']:
			self.energy += soil.soil[self.x][self.y]['plant_energy']
			soil.soil[self.x][self.y]['plant'] = None
			soil.soil[self.x][self.y]['plant_energy'] = 0
			soil.soil[self.x][self.y]['dung'] = True
		
		birth = False
		if self.energy >= 20:
			open_patch = self.detect(wild, soil, 'space')
			if len(open_patch) > 0:
				birth = self.reproduce(wild, open_patch)
		self.age += 1
		death = self.death()
		return (birth, death)

	def get_wild_range(self, wild, wild_range):
		for x, y in itertools.product([-1, 1], [-1, 1]):
			if (self.x + x, self.y + y) in wild.valid_wild:
				wild_range.append((self.x + x, self.y + y))
		return wild_range

	def sum_neuron_inputs(self, neuron):
		self.brain.nodes[neuron]['output'] = calc.activation(
			sum([
				(data['weight'] * self.brain.nodes[u_neuron]['output']) \
				for u_neuron, v_neuron, data in self.brain.edges(data=True) \
				if v_neuron == neuron]), 
				'tanh')

	def process_movement(self, wild):	
		axes = [['aMvX', 0], ['aMvY', 0]]
		for axis in axes:
			if axis[0] in self.brain.nodes:
				if self.brain.nodes[axis[0]]['output'] >= 0.9:
						axis[1] = 1
				elif self.brain.nodes[axis[0]]['output'] <= (-0.9):
						axis[1] = -1
		if (self.x + axes[0][1], self.y +a xes[1][1]) in self.wild_range:
			if wild.wild[self.x + axes[0][1]][self.y + axes[1][1]]['occupant'] == None:
				self.x += axes[0][1]
				self.y += axes[1][1]

	def reproduce(self, wild, open_patch):					
		x, y = random.sample(open_patch, 1)[0]		
		wild.animals.append(Animal(
			self.args, self.genome, self.neurons, x, y))
		wild.wild[x][y]['occupant'] = wild.animals[-1]
		self.energy -= 20
		return True
		
	def death(self):
		if self.age == 100:
			return True
		elif self.pain == 5:
			return True
		else:
			return False

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

	def detect_animal(self, wild, soil):
		nearby_animals = self.detect(wild, soil, 'animal')
		self.brain.nodes['sDtA']['output'] = (1 / 8) * nearby_animals

	def detect_plant(self, wild, soil):
		nearby_plants = self.detect(wild, soil, 'plant')
		self.brain.nodes['sDtP']['output'] = (1 / 8) * nearby_plants

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

	def decode_genome(self, mutation_chance=0.01):
		for gene in self.genome:
			if random.random() <= mutation_chance:
				gene = self.mutate(gene)
			self.colour.append([
				bitarray.util.ba2int(gene[0:8]),
				bitarray.util.ba2int(gene[8:16]),
				bitarray.util.ba2int(gene[16:24])])
			self.decode_gene(gene)
		self.colour = self.average_colour(self.colour)

	def mutate(self, gene):
		gene[random.sample([i for i in range(24)], 1)[0]] \
		= random.getrandbits(1)
		return gene

	def average_colour(self, colour):
		rgb = [0, 0, 0]
		for value in colour:
			for i in range(3):
				rgb[i] += value[i] 
		for i in range(3):
			rgb[i] = rgb[i] // len(colour)
		return rgb

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

	