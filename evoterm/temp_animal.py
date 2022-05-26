from dataclasses import dataclass
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
			self.population.append(Brain())

class Brain:

	def __init__(self):
		self.neurons = []
		self.genes = []
		self.species_id = None
		self.fitness = None


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
					gene = Gene(
						innovation_count,
						u_neuron,
						v_neuron,
						random.randrange(-20, 20) / 10,
						True,
						False)
					self.genes.append(gene)
					if innovation_count not in \
					[innovation.innovation for innovation in innovations]:
						innovations.append(gene)

					innovation_count += 1

	def add_neuron(self):
		pass

	def add_gene(self):
		pass

	def mutate(self):
		pass

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
		animals.species[count] = []
		index = random.sample(indexes, 1)[0]
		indexes.remove(index)
		animals.species[count].append(animals.population[index])
		animals.population[index].species_id = count
		
		for _, i in enumerate(indexes):
			if comparison_check(animals.species[count][0], animals.population[i]):
				animals.species[count].append(animals.population[i])
				animals.population[i].species_id = count
				to_remove.append(i)
		for i in to_remove:
			indexes.remove(i)
		count += 1






animals = Animals(
	input_n = 16, 
	hidden_n = 1, 
	output_n = 8, 
	percent_genes = 0.25)

animals.init_population(initial_population = 50)

for animal in animals.population:
	animal.initialise(
		animals.input_n, animals.hidden_n, animals.output_n,
		animals.percent_genes, animals.innovations, animals.innovation_count)

tmp = []
for animal in animals.population:
	if len(animal.genes) == 0:
		tmp.append(animal)
for animal in tmp:
	animals.population.remove(animal)


for animal in animals.population:
	animal.load_inputs()
	animal.run_network()

#for neuron in animals.population[0].neurons:
#	print(neuron)
for i, animal in enumerate(animals.population):
	print(f'Animal ID: {i}')
	for gene in animal.genes:		
		print(gene)

sort_species(animals)
print(len(animals.species))
print(animals.species)

