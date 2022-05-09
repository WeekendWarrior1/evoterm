from time import sleep
from class_creature import *
from functions_general import *
from plot import *

def main():

	internal_neurons = 4
	genes = 8
	neurons = {
		'00' : [0, 0, True, 'sDt'],
		'10' : [1, 0, True, 'aMx'],
		'11' : [1, 1, True, 'aMy']}

	neurons = {
		'sDet' : {'active':True, 'type':'sensory', 'index':0},
		'aMvX' : {'active':True, 'type':'action', 'index':0},
		'aMvY' : {'active':True, 'type':'action', 'index':1}}
	neurons = update_neurons_dict(neurons, internal_neurons)

	creatures = {i : Creature(random_genome(genes, neurons), neurons) for i in range(1)}
	print(creatures[0].neurons)
	for neuron in creatures[0].neurons:
		print(neuron)
	print(creatures[0].genome)
	print(creatures[0].brain.nodes)
	print(creatures[0].brain.edges(data=True))
	
	#plot(creatures[0], neurons)
	
	for i in range(100):
		clear()
		creatures[0].step()
		print(f'Current step: {i}')
		print('Current X: ' + str(creatures[0].pos_x))
		print(creatures[0].brain.nodes['aMvX']['output'])
		print('Current Y: ' + str(creatures[0].pos_y))
		print(creatures[0].brain.nodes['aMvY']['output'])
		print('Detect: ' + str(creatures[0].brain.nodes['sDet']['output']))
		print('i0: ' + str(creatures[0].brain.nodes['i0']['output']))
		print('i1: ' + str(creatures[0].brain.nodes['i1']['output']))

		sleep(0.1)
	
main()



