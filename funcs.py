from os import system, name
from random import sample
from time import sleep

def clear():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')

def normalise(value):
	if value < 128:
		return -(1.0 - (value / 128))
	else:
		return ((value - 127) / 128)

def update_neurons_dict(neurons, internal_neurons):
	updated_neurons = {}
	for neuron in neurons:
		if neurons[neuron]['active'] == True:
			updated_neurons[str(neuron)] = neurons[neuron]
	for i in range(internal_neurons):	
		updated_neurons[f'i{i}'] = {
			'active':True, 'type':'internal', 'index':i}
	return updated_neurons

def random_genome(genes, neurons):
	genome = []
	for i in range(genes):
		genome.append(random_gene(neurons))
	return genome

def random_gene(neurons, v_neuron=''):
	u_neuron = ''.join(sample(list(neurons), 1))
	if neurons[u_neuron]['type'] in ['sensory', 'internal']:
		u_neuron = (
			f'{0 if neurons[u_neuron]["type"] == "sensory" else 2}'
			f'{neurons[u_neuron]["index"]}')
		if len(v_neuron) == 0:
			v_neuron = ''.join(sample([
				neuron for neuron in neurons \
				if neurons[neuron]['type'] in ['action', 'internal']], 1))
			v_neuron = (
				f'{1 if neurons[v_neuron]["type"] == "action" else 2}'
				f'{neurons[v_neuron]["index"]}')
		weight = ''.join(sample('0123456789abcdef', 2))
		gene = ''.join((u_neuron, v_neuron, weight))
		return gene
	else:
		u_neuron = (
				f'{1}'
				f'{neurons[u_neuron]["index"]}')
		return random_gene(neurons, v_neuron=u_neuron)	

def test(cells, cell, duration=100):
	for i in range(duration):
		clear()
		cells[cell].step()

		print(
			f'Current step : {i}\n'
			f'Current x    : {cells[cell].pos_x}\n'
			f'aMvX output  : {cells[cell].brain.nodes["aMvX"]["output"]}\n'
			f'Current y    : {cells[cell].pos_y}\n'
			f'aMvY output  : {cells[cell].brain.nodes["aMvY"]["output"]}\n')

		sleep(0.1)				