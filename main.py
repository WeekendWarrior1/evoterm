from cell import *
from funcs import *
from plot import *

def main():

	internal_neurons = 4
	genes = 8
	neurons = {
		'sDet' : {'active':True, 'type':'sensory', 'index':0},
		'aMvX' : {'active':True, 'type':'action', 'index':0},
		'aMvY' : {'active':True, 'type':'action', 'index':1}}
	neurons = update_neurons_dict(neurons, internal_neurons)

	cells = {i : Cell(random_genome(genes, neurons), neurons) for i in range(1)}
	
	#plot(cells[0], neurons)

	test(cells, 0)
	
	
	
main()



