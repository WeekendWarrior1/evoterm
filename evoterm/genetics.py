import base64
import random
import bitarray

def populate_neurons(internal_neurons):
	neurons = {
		'sDtA' : {'type':'sensory', 'id':0},
		'sDtP' : {'type':'sensory', 'id':1},
		'sDpX' : {'type':'sensory', 'id':2},
		'sDnX' : {'type':'sensory', 'id':3},
		'sDpY' : {'type':'sensory', 'id':4},
		'sDnY' : {'type':'sensory', 'id':5},
		'sDpn' : {'type':'sensory', 'id':6},
		'aMvX' : {'type':'action', 'id':0},
		'aMvY' : {'type':'action', 'id':1}}
	
	for i in range(internal_neurons):	
		neurons[f'i{i}'] = {'type':'internal', 'id':i}
	
	return neurons


def encode_genome(neurons, genes, base64=0):
	if base64:
		return ''.join([\
			str(base64.b64encode(encode_gene(neurons).tobytes()))[2:6] \
			for i in range(genes)])
	else:
		return [encode_gene(neurons) for i in range(genes)]


def encode_gene(neurons):
	gene = bitarray.bitarray(12)
	
	for i in range(12):
		gene[i] = random.getrandbits(1)
	
	gene += encode_neuron(neurons, 'action')
	gene += encode_neuron(neurons, 'sensory')
	
	return gene


def encode_neuron(neurons, neuron_type):
	return bitarray.bitarray(random.getrandbits(1) for i in range(6))

