import base64, random
import bitarray

def populate_neurons(internal_neurons):
	neurons = {
		'sDet' : {'type':'sensory', 'id':0},
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
	neuron = bitarray.bitarray('000000')
	neuron[-1] = random.getrandbits(1)
	for i,e in enumerate(
		'{:b}'.format(neurons[random.sample([
		neuron for neuron in neurons \
		if neurons[neuron]['type'] \
		== ('internal' if neuron[-1] == 1 else neuron_type)], 1)[0]]\
		['id']), start=2):
		neuron[-i] = int(e)
	return neuron