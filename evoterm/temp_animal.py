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
class Synapse:
	innovation: int
	axon: int
	dendrite: int
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


def comparison_check(phenotype_a, phenotype_b, threshold=4):
	if compatability_distance(phenotype_a, phenotype_b) < threshold:
		return True
	else:
		return False


def compatability_distance(phenotype_a, phenotype_b, c1=1, c2=1, c3=0.4):
	phenotype_a_innovations = \
	[synapse.innovation for synapse in phenotype_a.brain.synapses]
	phenotype_b_innovations = \
	[synapse.innovation for synapse in phenotype_b.brain.synapses]
	if phenotype_a.fitness < phenotype_b.fitness:
		innovation_max = max(phenotype_b_innovations)
	else:
		innovation_max = max(phenotype_a_innovations)
	e = 0 # excess genes
	d = 0 # disjoint genes
	w = [] # average weight of shared genes between genotypes
	# (below) genotype with highest number of genes sets n if > 20, else 1
	if len(phenotype_a_innovations) >= len(phenotype_b_innovations):
		n = len(phenotype_a_innovations)
	else:
		n = len(phenotype_a_innovations)
	if n <= 20:
		n = 1

	for i, innovation in enumerate(phenotype_a_innovations):
		if phenotype_a.brain.synapses[i].enabled == True:
			if innovation not in phenotype_b_innovations:
				if innovation <= innovation_max:
					d += 1
				elif innovation > innovation_max:
					e += 1
	for i, innovation in enumerate(phenotype_a_innovations):	
		if innovation in phenotype_b_innovations:
			w.append(abs(phenotype_a.brain.synapses[i].weight))
	if len(w) == 0:
		w = 0
	else:
		w = sum(w) / len(w)

	for _, innovation in enumerate(phenotype_b_innovations):
		if innovation not in phenotype_a_innovations:
			if innovation <= innovation_max:
				d += 1
			elif innovation > innovation_max:
				e += 1

	compatability_distance = (((c1 * e) / n) + ((c2 * d) / n)) + (c3 * w)
	return compatability_distance


class Animals:

	def __init__(self):
		self.population = []
		self.species = {}
		self.genes = []
		self.gene_count = 0
		
	def init_population(self, 
		sensory_neurons, hidden_neurons, action_neurons,
		gene_chance, initial_population):
		
		for _ in range(initial_population):
			self.population.append(Animal())
		for animal in self.population:
			self.genes, self.gene_count = animal.brain.initialise(
				sensory_neurons, hidden_neurons, action_neurons,
				gene_chance, self.genes, self.gene_count)

		the_farm = [] # sends unviable animals (zero synapses) to "the farm"
		for animal in self.population:
			if len(animal.brain.synapses) == 0:
				the_farm.append(animal)
		for animal in the_farm:
			self.population.remove(animal)
		self.sort_species()

	def sort_species(self):
		indexes = [i for i, _ in enumerate(self.population)]
		count = 0

		while len(indexes):
			to_remove = []
			self.species[count] = Species(count)
			index = random.sample(indexes, 1)[0]
			indexes.remove(index)
			self.species[count].members.append(self.population[index])
			self.population[index].species_id = count
			
			for _, i in enumerate(indexes):
				#print(self.species[count].members[0].brain.synapses)
				#print(self.population[i].brain.synapses)
				if comparison_check(
					self.species[count].members[0], 
					self.population[i]):

					self.species[count].members.append(self.population[i])
					self.population[i].species_id = count
					to_remove.append(i)
			for i in to_remove:
				indexes.remove(i)
			count += 1


class Animal:

	def __init__(self):
		self.species_id = None
		self.fitness = 0
		self.fitness_adjusted = 0
		self.brain = Brain()
		self.energy = 0
		self.age = 0


class Brain:

	def __init__(self):
		self.neurons = []
		self.synapses = []
		
	def initialise(self, 
		sensory_neurons, hidden_neurons, action_neurons, 
		gene_chance, genes, gene_count):
		
		count = 0
		for i in range(sensory_neurons):
			count += 1
			self.neurons.append(Neuron(count, 1, 1, 0, 0))
		for i in range(action_neurons):
			count += 1
			self.neurons.append(Neuron(count, 2, 3, 0, 0))
		for i in range(hidden_neurons):
			count += 1
			self.neurons.append(Neuron(count, 0, 2, 0, 0))
		for hidden_neuron in [_ for _ in self.neurons if _.kind == 0]:
			for sa_neuron in [_ for _ in self.neurons if _.kind in [1, 2]]:
				if random.random() > gene_chance:
					if sa_neuron.kind == 1:
						axon = sa_neuron._id
						dendrite = hidden_neuron._id
					elif sa_neuron.kind == 2:
						axon = hidden_neuron._id
						dendrite = sa_neuron._id
					genes, gene_count = self.establish_synapse(
						axon, dendrite, 
						random.randrange(-20, 20) / 10,
						genes, gene_count)	
		genes, gene_count = self.mutate(genes, gene_count)

		return genes, gene_count
	
	def establish_synapse(self, 
		axon, dendrite, weight, genes, gene_count, 
		enabled=True, recurrent=False):
		
		def check_genes(axon, dendrite, genes):
			for gene in genes:
				if axon == gene.axon and dendrite == gene.dendrite:
					return gene
			return None

		synapse = check_genes(axon, dendrite, genes)
		if synapse:
			synapse = Synapse(
				synapse.innovation,
				synapse.axon,
				synapse.dendrite,
				weight,
				enabled,
				recurrent)
		else:
			synapse = Synapse(
				gene_count,
				axon,
				dendrite,
				weight,
				enabled,
				recurrent)
			genes.append(synapse)
			gene_count += 1
		self.synapses.append(synapse)
		return genes, gene_count

	def mutate(self, genes, gene_count):
		for synapse in self.synapses:
			if random.random() <= 0.001:
				if random.random() <= 0.9:
					if random.random() <= 0.5:
						synapse.weight += synapse.weight * 0.2
					else:
						synapse.weight -= synapse.weight * 0.2
				else: 
					synapse.weight = random.randrange(-20, 20) / 10
		if random.random() <= 0.05:
			genes, gene_count = self.add_synapse(genes, gene_count)
		if random.random() <= 0.05:
			genes, gene_count = self.add_neuron(genes, gene_count)
		return genes, gene_count

	def add_synapse(self, genes, gene_count):
		def random_neuron_pair(count):
			if count == 20:
				return None, None
			axon = random.sample(self.neurons, 1)[0]
			dendrite = random.sample(self.neurons, 1)[0]
			if axon._id == dendrite._id:
				return random_neuron_pair(count)
			if axon.layer >= dendrite.layer:
				return random_neuron_pair(count)
			else:
				return axon, dendrite

		axon, dendrite = random_neuron_pair(0)

		if axon == None:
			return genes, gene_count
		for synapse in self.synapses:
			if synapse.axon == axon._id and synapse.dendrite == dendrite._id:
				if random.random() <= 0.25:
					if synapse.enabled == False:
						synapse.enabled = True
				return genes, gene_count
		
		genes, gene_count = self.establish_synapse(
			axon._id, dendrite._id, random.randrange(-20, 20) / 10,
			genes, gene_count)
		return genes, gene_count

	def add_neuron(self, genes, gene_count):
		random_synapse = random.sample(self.synapses, 1)[0]
		random_synapse.enabled = False
		neuron_len = len(self.neurons)
		new_neuron = Neuron(neuron_len, 0, None, 0, 0)
		self.neurons.append(new_neuron)

		# back half of new neuron
		genes, gene_count = self.establish_synapse(
			random_synapse.axon, new_neuron._id, 
			random_synapse.weight,
			genes, gene_count)

		# forward half of new neuron
		genes, gene_count = self.establish_synapse(
			new_neuron._id, random_synapse.dendrite, 
			random.randrange(-20, 20) / 10,
			genes, gene_count)

		edges = []
		for synapse in self.synapses:
			if synapse.enabled == True:
				edges.append([synapse.axon, synapse.dendrite])

		G = calc.generate_topology(edges)

		for neuron in self.neurons:
			if neuron.kind == 0:
				all_paths = calc.DFS(G, neuron._id)
				max_len_path = max(len(p) for p in all_paths)
				neuron.layer = 1 + max_len_path

		return genes, gene_count

	def load_inputs(self):
		for neuron in self.neurons: 
			if neuron.layer == 1:
				neuron.sum_output = neuron.sum_input

	def run_network(self):
		for layer, neuron in itertools.product([1, 2], self.neurons):
			if neuron.layer == layer:
				neuron.sum_input = 0
				for synapse in self.synapses: 
					if synapse.dendrite == neuron._id:
						neuron.sum_input += \
						self.neurons[synapse.axon].sum_output * synapse.weight
				neuron.sum_output = calc.activation(neuron.sum_input, 'tanh')

	def get_output(self, neuron):
		return neuron.sum_output

	









"""
sensory_neurons = 12
hidden_neurons = 1
action_neurons = 4
gene_chance = 0.25
initial_population = 100

animals = Animals()
animals.init_population(
	sensory_neurons, hidden_neurons, action_neurons,
	gene_chance, initial_population)

for animal in animals.population:
	animal.brain.load_inputs()
	animal.brain.run_network()

print(len(animals.species))"""


