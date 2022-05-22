from dataclasses import dataclass
import math
import random

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
	in_node_id: int
	out_node_id: int
	weight: float
	enabled: bool
	recurrent: bool

class Animals:

	def __init__(self, pop_size, input_n, hidden_n, output_n):
		self.pop_size = pop_size
		self.input_n = input_n
		self.hidden_n = hidden_n
		self.output_n = output_n
		self.percent_connections = 0.25

class Brain:

	def __init__(self, input_n, hidden_n, output_n, percent_connections):
		self.nodes = []
		self.connections = []
		self.initialise(input_n, hidden_n, output_n, percent_connections)

	def initialise(self, input_n, hidden_n, output_n, percent_connections):
		count = 0
		# bias node
		self.nodes.append(Node(count, 3, 1, 0, 0))
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
			for node in [node for node in self.nodes if node.kind == 1 or 2]:
				if random.random() <= percent_connections:
					innovation_id = f'{hidden.identifier}{node.identifier}'
					zeroes = ''
					for _ in range(4 - len(innovation_id)):
						zeroes += '0'
					innovation_id = innovation_id[:1] + zeroes + innovation_id[1:]
					self.connections.append(Connection(
						int(innovation_id),
						node.identifier,
						hidden.identifier,
						random.randrange(-20, 20) / 10,
						True,
						False
						))

	def add_node(self):
		pass

	def add_connection(self):
		pass

	def mutate(self):
		pass

	def load_inputs(self):
		for node in self.nodes: 
			if node.kind == 1:
				node.sum_output = node.sum_input

	def run_network(self):
		
		for node in self.nodes: 
			if node.kind == 2:
				running_sum = 0
				node.sum_input = 0
				for connection in self.connections: 
					if connection.out_node_id == node.identifier:
						running_sum += self.nodes[connection.in_node_id].sum_output * connection.weight
				node.sum_output = running_sum

animal = Brain(4, 1, 3, 0.25)
#print(animal.nodes)
print(animal.connections)
animal.load_inputs
animal.run_network
print(animal.nodes)


