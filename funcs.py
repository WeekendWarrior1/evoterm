import argparse
import networkx as nx
import matplotlib.pyplot as plt
from os import system, name
from math import tanh
from random import sample, getrandbits
from time import sleep


def clear():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-g', '--genes', 
		metavar='', type=int, nargs='?', const=4, help='number of genes')
	parser.add_argument(
		'-n', '--neurons', 
		metavar='', type=int, nargs='?', const=2, help='number of internal neurons')
	parser.add_argument(
		'-c', '--cells',
		metavar='', type=int, nargs='?', const=1, help='number of cells')
	return parser.parse_args()	


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


def populate_neurons(internal_neurons):
	neurons = {
		'sDet' : {'type':'sensory', 'index':0},
		'aMvX' : {'type':'action', 'index':0},
		'aMvY' : {'type':'action', 'index':1}}
	for i in range(internal_neurons):	
		neurons[f'i{i}'] = {'type':'internal', 'index':i}
	return neurons


def genome(neurons, genes):
	return [gene(neurons) for i in range(genes)]


def gene(neurons, v_neuron=''):
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
		return gene(neurons, v_neuron=f'{1}{neurons[u_neuron]["index"]}')


def plot(cell, neurons):
	e_positive = \
	[(u, v) for (u, v, d) in cell.brain.edges(data=True) if d["weight"] > 0.0]
	e_negative = \
	[(u, v) for (u, v, d) in cell.brain.edges(data=True) if d["weight"] <= 0.0]

	# positions for all nodes - seed for reproducibility
	pos = nx.spring_layout(cell.brain, seed=7)  

	# nodes
	nx.draw_networkx_nodes(cell.brain, pos, node_size=700)

	# edges
	nx.draw_networkx_edges(
		cell.brain, pos, edgelist=e_positive, width=6, edge_color="tab:green")
	nx.draw_networkx_edges(
	    cell.brain, pos, edgelist=e_negative, width=6, edge_color="tab:red")

	# labels
	nx.draw_networkx_labels(
		cell.brain, pos, font_size=12, font_family="sans-serif")

	ax = plt.gca()
	ax.margins(0.08)
	plt.axis("off")
	plt.tight_layout()
	plt.show()	


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