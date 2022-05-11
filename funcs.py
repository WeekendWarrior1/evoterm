from os import system, name
from math import tanh
from random import sample, getrandbits
from time import sleep


def clear():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')

def normalise(x):
	if x < 128:
		return -(1.0 - (x / 128))
	else:
		return ((x - 127) / 128)

def activation(x, func, bias=1):
	if func == 'tanh':
		return (tanh(x) + bias) / 2
	elif func == 'ReLU':
		return (max(0, x) + bias) / 2

def update_neurons_dict(neurons, internal_neurons):
	updated_neurons = {}
	for neuron in neurons:
		if neurons[neuron]['active']:
			updated_neurons[str(neuron)] = neurons[neuron]
	for i in range(internal_neurons):	
		updated_neurons[f'i{i}'] = {
			'active':True, 'type':'internal', 'index':i}
	return updated_neurons

def random_genome(genes, neurons):
	return [random_gene(neurons) for i in range(genes)]

def random_gene(neurons, v_neuron=''):
	u_neuron = sample([*neurons], 1)[0]
	if neurons[u_neuron]['type'] != 'action':
		u_neuron = (
			f'{0 if neurons[u_neuron]["type"] == "sensory" else 2}'
			f'{neurons[u_neuron]["index"]}')
		if not v_neuron:
			v_neuron = sample([
				neuron for neuron in neurons \
				if neurons[neuron]['type'] != 'sensory'], 1)[0]
			v_neuron = (
				f'{1 if neurons[v_neuron]["type"] == "action" else 2}'
				f'{neurons[v_neuron]["index"]}')
		return f'{u_neuron}{v_neuron}{"%0x" % getrandbits(8)}'
	else:
		return random_gene(neurons, v_neuron=f'{1}{neurons[u_neuron]["index"]}')	

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