from dataclasses import dataclass
import math
import random
import calc

@dataclass
class Node:
	identifier: int
	kind: int
	layer: int
	sum_input: float
	sum_output: float

@dataclass
class Connection:
	innovation_id: int
	u_neuron_id: int
	v_neuron_id: int
	weight: float
	enabled: bool
	recurrent: bool

class Animals:

	def __init__(self, input_n, hidden_n, output_n, percent_connections):
		self.input_n = input_n
		self.hidden_n = hidden_n
		self.output_n = output_n
		self.population = []
		self.innovations = []
		self.percent_connections = percent_connections
		self.innovation_count = 0
		

	def init_population(self, pop_size):
		for _ in range(pop_size):
			self.population.append(Brain())

class Brain:

	def __init__(self):
		self.nodes = []
		self.connections = []
		self.species_id = None
		self.fitness = None


	def initialise(self, input_n, hidden_n, output_n, 
		percent_connections, innovations, innovation_count):
		count = 0
		for i in range(input_n):
			count += 1
			self.nodes.append(Node(count, 1, 1, 0, 0))
		for i in range(output_n):
			count += 1
			self.nodes.append(Node(count, 2, 3, 0, 0))
		for i in range(hidden_n):
			count += 1
			self.nodes.append(Node(count, 0, 2, 0, 0))
		for hidden in [node for node in self.nodes if node.kind == 0]:
			for node in [node for node in self.nodes if node.kind in [1, 2]]:
				if random.random() <= percent_connections:
					if node.kind == 1:
						u_neuron = node.identifier
						v_neuron = hidden.identifier
					elif node.kind == 2:
						u_neuron = hidden.identifier
						v_neuron = node.identifier
					connection = Connection(
						innovation_count,
						u_neuron,
						v_neuron,
						random.randrange(-20, 20) / 10,
						True,
						False)
					self.connections.append(connection)
					if innovation_count not in [innovation.innovation_id for innovation in innovations]:
						innovations.append(connection)

					innovation_count += 1

	def add_node(self):
		pass

	def add_connection(self):
		pass

	def mutate(self):
		pass

	def load_inputs(self):
		for node in self.nodes: 
			if node.layer == 1:
				node.sum_output = node.sum_input

	def run_network(self):
		for layer in [1, 2]:
			for node in self.nodes: 
				if node.layer == layer:
					node.sum_input = 0
					for connection in self.connections: 
						if connection.v_neuron_id == node.identifier:
							node.sum_input += self.nodes[connection.u_neuron_id].sum_output * connection.weight
					node.sum_output = calc.activation(node.sum_input, 'tanh')

	def get_output(self, node):
		return node.sum_output


def compatability_distance(genotype_a, genotype_b):
	if genotype_a.fitness > genotype_b:
		dom_parent = genotype_a
		sub_parent = genotype_b
	elif genotype_a.fitness < genotype_b.fitness:
		dom_parent = genotype_b
		sub_parent = genotype_a
	elif genotype_a.fitness == genotype_b.fitness:
		fit_parent = both
	innovation_max = max([connection.innovation_id for connection in dom_parent.connections])

	shared_genes = []
	disjoint_genes = []
	excess_genes = []

	for connection in sub_parent.connections:
		if connection.innovation_id <= innovation_max:
			if connection.innovation_id in dom_parent.connections:	
				shared_genes.append(connection)
			elif connection.innovation_id not in dom_parent.connections:
				disjoint_genes.append(connection)
		elif connection.innovation_id > innovation_max:
			excess_genes.append(connection)
		 



	CD = E + D + avgW

animals = Animals(
	input_n = 4, 
	hidden_n = 1, 
	output_n = 3, 
	percent_connections = 0.25)

animals.init_population(pop_size = 50)

for animal in animals.population:
	animal.initialise(
		animals.input_n, animals.hidden_n, animals.output_n,
		animals.percent_connections, animals.innovations, animals.innovation_count)

for animal in animals.population:
	animal.load_inputs()
	animal.run_network()

for node in animals.population[0].nodes:
	print(node)
for connection in animals.population[0].connections:
	print(connection)


