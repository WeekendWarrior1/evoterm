from cell import *
from funcs import *


def main():
	args = get_args()
	neurons = populate_neurons(args.neurons)
	cells = {}
	
	#for i in range(args.cells):
	#	cells[i] = Cell(genome(neurons, args.genes), neurons)
	print(encode_genome(neurons, args.genes))
	print(encode_genome(neurons, args.genes, 1))

	#plot(cells[0], neurons)
	#test(cells, 0)
	

if __name__ == '__main__':
	main()



