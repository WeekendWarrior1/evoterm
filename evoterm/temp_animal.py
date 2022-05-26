from collections import defaultdict
from dataclasses import dataclass, field
import itertools
import math
import random
import calc

@dataclass
class Neuron:
	_id: int
	kind: int
	layer: int
	sum_input: float
	sum_output: float

@dataclass
class Gene:
	innovation: int
	u_neuron_id: int
	v_neuron_id: int
	weight: float
	enabled: bool
	recurrent: bool

@dataclass
class Species:
	_id: int
	members: list = field(default_factory=lambda : [])
	fitness: float = 0
	fitness_adjusted: float = 0
	fitness_sum: float = 0
	generations_since_improvement: int = 0

class Animals:

	def __init__(self, input_n, hidden_n, output_n, percent_genes):
		self.input_n = input_n
		self.hidden_n = hidden_n
		self.output_n = output_n
		self.population = []
		self.species = {}
		self.innovations = []
		self.percent_genes = percent_genes
		self.innovation_count = 0
		

	def init_population(self, initial_population):
		for _ in range(initial_population):
			self.population.append(Animal())


class Animal:

	def __init__(self):
		self.species_id = None
		self.fitness = lambda x, y : x / y
		self.fitness_adjusted = lambda x, y, z : (x / y) / z
		self.brain = Brain()
		self.energy = 0
		self.age = 0


class Brain:

	def __init__(self):
		self.neurons = []
		self.genes = []
		
	def initialise(self, input_n, hidden_n, output_n, 
		percent_genes, innovations, innovation_count):
		count = 0
		for i in range(input_n):
			count += 1
			self.neurons.append(Neuron(count, 1, 1, 0, 0))
		for i in range(output_n):
			count += 1
			self.neurons.append(Neuron(count, 2, 3, 0, 0))
		for i in range(hidden_n):
			count += 1
			self.neurons.append(Neuron(count, 0, 2, 0, 0))
		for hidden_neuron in [_ for _ in self.neurons if _.kind == 0]:
			for io_neuron in [_ for _ in self.neurons if _.kind in [1, 2]]:
				if random.random() <= percent_genes:
					if io_neuron.kind == 1:
						u_neuron = io_neuron._id
						v_neuron = hidden_neuron._id
					elif io_neuron.kind == 2:
						u_neuron = hidden_neuron._id
						v_neuron = io_neuron._id
					gene = self.check_innovations(u_neuron, v_neuron, innovations)
					if gene:
						gene = Gene(
							gene.innovation,
							gene.u_neuron_id,
							gene.v_neuron_id,
							random.randrange(-20, 20) / 10,
							True,
							False)
					else:
						gene = Gene(
							innovation_count,
							u_neuron,
							v_neuron,
							random.randrange(-20, 20) / 10,
							True,
							False)
						innovations.append(gene)
						innovation_count += 1
					self.genes.append(gene)
					
		return innovations, innovation_count
		
	def mutate(self, innovations, innovation_count):
		for gene in self.genes:
			if random.random() <= 0.001:
				if random.random() <= 0.9:
					if random.random() <= 0.5:
						gene.weight += gene.weight * 0.2
					else:
						gene.weight -= gene.weight * 0.2
				else: 
					gene.weight = random.randrange(-20, 20) / 10
		if random.random() <= 0.05:
			innovations, innovation_count = self.add_connection(innovations, innovation_count)
		if random.random() <= 0.05:
			innovations, innovation_count = self.add_node(innovations, innovation_count)
		return innovations, innovation_count

	def add_node(self, innovations, innovation_count):
		random_gene = random.sample(self.genes, 1)[0]
		random_gene.enabled = False
		new_neuron = Neuron(len(self.neurons), 0, None, 0, 0)
		self.neurons.append(new_neuron)

		# back half of new neuron
		gene = self.check_innovations(random_gene.u_neuron_id, new_neuron._id, innovations)
		if gene:
			self.genes.append(Gene(
				gene.innovation,
				gene.u_neuron_id,
				new_neuron._id,
				random_gene.weight,
				True,
				False))
		else:
			gene = Gene(
				innovation_count,
				random_gene.u_neuron_id,
				new_neuron._id,
				random_gene.weight,
				True,
				False)
			self.genes.append(gene)
			innovations.append(gene)
			innovation_count += 1

		# forward half of new neuron
		gene = self.check_innovations(new_neuron._id, random_gene.v_neuron_id, innovations)
		if gene:
			self.genes.append(Gene(
				gene.innovation,
				new_neuron._id,
				gene.v_neuron_id,
				random.randrange(-20, 20) / 10,
				True,
				False))
		else:
			gene = Gene(
				innovation_count,
				new_neuron._id,
				random_gene.v_neuron_id,
				random.randrange(-20, 20) / 10,
				True,
				False)
			self.genes.append(gene)
			innovations.append(gene)
			innovation_count += 1

		G = self.generate_topology()

		for neuron in self.neurons:
			if neuron.kind == 0:
				all_paths = self.DFS(G, neuron._id)
				max_len_path = max(len(p) for p in all_paths)
				neuron.layer = 1 + max_len_path

		return innovations, innovation_count
				
	def generate_topology(self):
		""" copied from:
		https://stackoverflow.com/questions/29320556/finding-longest-path-in-a-graph
		"""
		edges = []
		for gene in self.genes:
			if gene.enabled == True:
				edges.append([gene.u_neuron_id, gene.v_neuron_id])
		G = defaultdict(list)
		for (s, t) in edges:
			G[s].append(t)
			G[t].append(s)
		return G

	def DFS(self, G, v, seen=None, path=None):
		""" copied from:
		https://stackoverflow.com/questions/29320556/finding-longest-path-in-a-graph
		"""
		if seen is None: seen = []
		if path is None: path = [v]

		seen.append(v)

		paths = []
		for t in G[v]:
			if t not in seen:
				t_path = path + [t]
				paths.append(tuple(t_path))
				paths.extend(self.DFS(G, t, seen[:], t_path))
		return paths

	def check_innovations(self, u_neuron, v_neuron, innovations):
		for gene in innovations:
			if u_neuron == gene.u_neuron_id and v_neuron == gene.v_neuron_id:
				return gene
		return None

	def add_connection(self, innovations, innovation_count):
		def random_neuron_pair(count):
			if count == 20:
				return None, None
			u_neuron = random.sample(self.neurons, 1)[0]
			v_neuron = random.sample(self.neurons, 1)[0]
			if u_neuron._id == v_neuron._id:
				return random_neuron_pair(count)
			if u_neuron.layer >= v_neuron.layer:
				return random_neuron_pair(count)
			else:
				return u_neuron, v_neuron

		u_neuron, v_neuron = random_neuron_pair(0)

		if u_neuron == None:
			return None
		for gene in self.genes:
			if gene.u_neuron_id == u_neuron and gene.v_neuron_id == v_neuron:
				if random.random() <= 0.25:
					if gene.enabled == False:
						gene.enabled = True
				return None
		
		gene = self.check_innovations(u_neuron, v_neuron, innovations)
		if gene:
			self.genes.append(Gene(
				gene.innovation,
				gene.u_neuron_id,
				gene.v_neuron_id,
				random.randrange(-20, 20) / 10,
				True,
				False))
		else:
			gene = Gene(
				innovation_count,
				u_neuron._id,
				v_neuron._id,
				random.randrange(-20, 20) / 10,
				True,
				False)
			self.genes.append(gene)
			innovations.append(gene)
			innovation_count += 1
		return innovations, innovation_count

	def load_inputs(self):
		for neuron in self.neurons: 
			if neuron.layer == 1:
				neuron.sum_output = neuron.sum_input

	def run_network(self):
		for layer, neuron in itertools.product([1, 2], self.neurons):
			if neuron.layer == layer:
				neuron.sum_input = 0
				for gene in self.genes: 
					if gene.v_neuron_id == neuron._id:
						neuron.sum_input += \
						self.neurons[gene.u_neuron_id].sum_output * gene.weight
				neuron.sum_output = calc.activation(neuron.sum_input, 'tanh')

	def get_output(self, neuron):
		return neuron.sum_output


def compatability_distance(genotype_a, genotype_b, c1=1, c2=1, c3=0.4):
	genotype_a_genes = [gene.innovation for gene in genotype_a.genes]
	genotype_b_genes = [gene.innovation for gene in genotype_b.genes]
	innovation_max = max(genotype_b_genes)
	e = 0 # excess genes
	d = 0 # disjoint genes
	w = [] # average weight of shared genes between genotypes
	# (below) genotype with highest number of genes sets n if > 20, else 1
	if len(genotype_a_genes) >= len(genotype_b_genes):
		n = len(genotype_a_genes)
	else:
		n = len(genotype_b_genes)
	if n <= 20:
		n = 1

	for i, gene in enumerate(genotype_a_genes):
		if genotype_a.genes[i].enabled == True:
			if gene not in genotype_b_genes:
				if gene <= innovation_max:
					d += 1
				elif gene > innovation_max:
					e += 1
	for i, gene in enumerate(genotype_a_genes):	
		if gene in genotype_b_genes:
			w.append(abs(genotype_a.genes[i].weight))
	if len(w) == 0:
		w = 0
	else:
		w = sum(w) / len(w)

	for _, gene in enumerate(genotype_b_genes):
		if gene not in genotype_a_genes:
			if gene <= innovation_max:
				d += 1
			elif gene > innovation_max:
				e += 1

	compatability_distance = (((c1 * e) / n) + ((c2 * d) / n)) + (c3 * w)
	return compatability_distance


def comparison_check(genotype_a, genotype_b, threshold=4):
	if compatability_distance(genotype_a, genotype_b) < threshold:
		return True
	else:
		return False

def sort_species(animals):
	indexes = [i for i, _ in enumerate(animals.population)]
	count = 0

	while len(indexes):
		to_remove = []
		animals.species[count] = Species(count)
		index = random.sample(indexes, 1)[0]
		indexes.remove(index)
		animals.species[count].members.append(animals.population[index])
		animals.population[index].species_id = count
		
		for _, i in enumerate(indexes):
			if comparison_check(animals.species[count].members[0].brain, animals.population[i].brain):
				animals.species[count].members.append(animals.population[i])
				animals.population[i].species_id = count
				to_remove.append(i)
		for i in to_remove:
			indexes.remove(i)
		count += 1






animals = Animals(
	input_n = 12, 
	hidden_n = 1, 
	output_n = 4, 
	percent_genes = 0.25)

animals.init_population(initial_population = 1000)

for animal in animals.population:
	animals.innovations, animals.innovation_count = animal.brain.initialise(
		animals.input_n, animals.hidden_n, animals.output_n,
		animals.percent_genes, animals.innovations, animals.innovation_count)

tmp = []
for animal in animals.population:
	if len(animal.brain.genes) == 0:
		tmp.append(animal)
for animal in tmp:
	animals.population.remove(animal)
for animal in animals.population:
	animals.innovations, animals.innovation_count = animal.brain.mutate(animals.innovations, animals.innovation_count)

tmp = []
for animal in animals.population:
	dead_gene = 0
	for gene in animal.brain.genes:
		if gene.enabled == False:
			dead_gene += 1
	if len(animal.brain.genes) == dead_gene:
		tmp.append(animal)
for animal in tmp:
	animals.population.remove(animal)

for animal in animals.population:
	animal.brain.load_inputs()
	animal.brain.run_network()


#for i, animal in enumerate(animals.population):
#	print(f'Animal ID: {i}')
#	for gene in animal.brain.genes:		
#		print(gene)

sort_species(animals)
print(len(animals.species))


