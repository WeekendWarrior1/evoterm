import random
import itertools
import networkx as nx 
import bitarray
import bitarray.util
import calc
import genetics


class Cell:
	
	def __init__(self, genome, neurons, x=0, y=0):
		self.brain = nx.DiGraph()
		self.neurons = neurons
		self.genome = genome
		self.colour = []
		self.decode_genome()
		self.neuron_functions = {
			'sDet' : self.process_detect
		}
		self.x = x
		self.y = y

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
	
	def fire_neurons(self, cells, index, env_size, coordinates):
		self.check_sensory(coordinates)
		
		for neuron in self.brain.nodes:
			if self.neurons[neuron]['type'] in ['internal', 'action']:
				self.sum_neuron_inputs(neuron)
		
		self.process_movement(coordinates, env_size)
		self.reproduce(cells, coordinates)
		return self.death()

	def check_sensory(self, coordinates):
		for neuron in self.brain.nodes: 
			if self.neurons[neuron]['type'] == 'sensory':
				self.neuron_functions[neuron](coordinates)

	def sum_neuron_inputs(self, neuron):
		self.brain.nodes[neuron]['output'] = calc.activation(
			sum([
				(data['weight'] * self.brain.nodes[u_neuron]['output']) \
				for u_neuron, v_neuron, data in self.brain.edges(data=True) \
				if v_neuron == neuron]), 
			'tanh')

	def process_movement(self, coordinates, env_size):	
		neuron_data = [['aMvX', 0, self.x], ['aMvY', 0, self.y]]
		for data in neuron_data:
			if data[0] in self.brain.nodes:
				if self.brain.nodes[data[0]]['output'] >= 0.9:
					if (data[2] + 1) <= env_size:
						data[1] = 1
				elif self.brain.nodes[data[0]]['output'] <= (-0.9):
					if (data[2] - 1) >= 1:
						data[1] = -1

		if coordinates\
		[self.x + neuron_data[0][1]]\
		[self.y + neuron_data[1][1]]\
		['occupied'] == False:
			self.x += neuron_data[0][1]
			self.y += neuron_data[1][1]

	def process_detect(self, coordinates):
		presence = 0
		open_space = []
		for x, y in itertools.product(range(-1, 2), range(-1, 2)):
			if x != 0 and y != 0:
				if coordinates[self.x + x][self.y + y]['occupied'] == True:
					presence += 1
				elif coordinates[self.x + x][self.y + y]['occupied'] == False:
					open_space.append((self.x + x, self.y + y))
		self.brain.nodes['sDet']['output'] = (1 / 8) * presence
		return open_space

	def reproduce(self, cells, coordinates):
		if random.randint(0, 100) == 0:
			open_space = self.process_detect(coordinates)
			if len(open_space) != 0:
				x, y = random.sample(open_space, 1)[0]
				cells.append(Cell(self.genome, self.neurons, x, y))
				print(
					term.move_xy(cells[-1].x, cells[-1].y) + 
					term.color_rgb(cells[-1].colour[0], cells[-1].colour[1], cells[-1].colour[2]) + 
					char)

				coordinates[x][y]['occupied'] = True
				coordinates[x][y]['occupant'] = cells[-1]

	def death(self):
		if random.randint(0, 100) == 0:
			"""coordinates[self.x][self.y]['occupied'] = False
			coordinates[self.x][self.y]['occupant'] = None
			del cells[index]"""
			return True
